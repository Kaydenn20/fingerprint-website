from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from tensorflow.keras.models import load_model
# Import the correct preprocess_input for ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras import Model
from tensorflow.keras.layers import Input
import tensorflow as tf
from PIL import Image
import cv2
import numpy as np
import os
import base64
import io
import datetime

app = Flask(__name__)
# Configure CORS to allow requests from your frontend
CORS(app, resources={
    r"/predict": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173", "*"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Load the trained model
# Make sure 'model.keras' is the correct path to your saved ResNet model
model = load_model("model.resnet.keras")

# Define the labels based on your Resnet.ipynb notebook
# This maps the model's output index to the blood group label
labels = {0: 'A+', 1: 'A-', 2: 'AB+', 3: 'AB-', 4: 'B+', 5: 'B-', 6: 'O+', 7: 'O-'}

# --- Real-time stats storage ---
prediction_stats = {
    'total': 0,
    'blood_groups': {},  # e.g., {'A+': 5, 'O-': 2, ...}
    'confidences': [],    # list of floats
    'recent_predictions': []  # list of dicts: {blood_group, confidence, timestamp}
}

def generate_gradcam(model, img_array, predicted_class, layer_name=None):
    """
    Generate Grad-CAM visualization for the predicted class
    """
    try:
        # Create a model that outputs both the predictions and the last convolutional layer
        if layer_name is None:
            # Try to find the last convolutional layer automatically
            for layer in reversed(model.layers):
                if 'conv' in layer.name.lower() or 'add' in layer.name.lower():
                    layer_name = layer.name
                    break
        
        if layer_name is None:
            # Fallback to a common ResNet layer name
            layer_name = 'conv5_block3_out'
        
        # Create a model that outputs both the predictions and the target layer
        grad_model = Model(
            inputs=[model.inputs],
            outputs=[model.get_layer(layer_name).output, model.output]
        )
        
        # Compute the gradient of the top predicted class for our input image
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, predicted_class]
        
        # Extract the gradients of the top predicted class with regard to
        # the output feature map of the last conv layer
        grads = tape.gradient(loss, conv_outputs)
        
        # Vector-mean of the gradients over the batch dimension
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight the channels by their mean gradient values
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize the heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        
        # Resize the heatmap to the original image size
        heatmap = cv2.resize(heatmap, (256, 256))
        
        # Convert heatmap to RGB
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        # Convert BGR to RGB
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # Superimpose the heatmap on original image
        # Convert original image to RGB if needed
        original_img = img_array[0]
        if len(original_img.shape) == 3 and original_img.shape[2] == 3:
            # Normalize original image to 0-255 range
            original_img = ((original_img - original_img.min()) / 
                          (original_img.max() - original_img.min()) * 255).astype(np.uint8)
        
        # Create overlay
        overlay = heatmap * 0.4 + original_img * 0.6
        overlay = np.clip(overlay, 0, 255).astype(np.uint8)
        
        return overlay, heatmap
        
    except Exception as e:
        print(f"Error generating Grad-CAM: {e}")
        return None, None

def encode_image_to_base64(image_array):
    """
    Convert numpy array to base64 encoded string
    """
    try:
        # Convert to PIL Image
        img = Image.fromarray(image_array)
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Encode to base64
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def is_likely_fingerprint(image_array):
    """
    Strict heuristic to check if an image is likely a fingerprint
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        
        # Calculate image statistics
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Calculate edge density (fingerprints have many edges)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Calculate local binary pattern or texture features
        # Simple texture measure using variance of local regions
        texture_score = 0
        for i in range(0, gray.shape[0]-8, 8):
            for j in range(0, gray.shape[1]-8, 8):
                patch = gray[i:i+8, j:j+8]
                texture_score += np.var(patch)
        texture_score /= ((gray.shape[0]//8) * (gray.shape[1]//8))
        
        # Calculate ridge frequency (fingerprints have regular ridge patterns)
        # Use FFT to detect periodic patterns
        fft = np.fft.fft2(gray)
        fft_shift = np.fft.fftshift(fft)
        magnitude_spectrum = np.log(np.abs(fft_shift) + 1)
        
        # Calculate the energy in mid-frequency bands (where fingerprint ridges appear)
        center_y, center_x = magnitude_spectrum.shape[0] // 2, magnitude_spectrum.shape[1] // 2
        mid_freq_energy = 0
        for i in range(center_y-20, center_y+20):
            for j in range(center_x-20, center_x+20):
                if 0 <= i < magnitude_spectrum.shape[0] and 0 <= j < magnitude_spectrum.shape[1]:
                    mid_freq_energy += magnitude_spectrum[i, j]
        mid_freq_energy /= 1600  # Normalize by the area
        
        # Calculate aspect ratio (fingerprints are usually more square-ish)
        aspect_ratio = gray.shape[1] / gray.shape[0]
        
        # STRICT Fingerprint characteristics:
        # 1. High edge density (fingerprints have many ridges and valleys)
        # 2. Very high texture variance (detailed ridge patterns)
        # 3. Moderate intensity (not too bright or dark)
        # 4. High mid-frequency energy (periodic ridge patterns)
        # 5. Reasonable aspect ratio (not too wide or tall)
        # 6. High standard deviation (good contrast)
        
        is_fingerprint = (
            edge_density > 0.08 and           # Increased from 0.05 - at least 8% of pixels are edges
            texture_score > 800 and           # Increased from 500 - very high texture variance
            60 < mean_intensity < 180 and     # Tighter brightness range
            mid_freq_energy > 8.0 and         # High mid-frequency energy for ridge patterns
            0.7 < aspect_ratio < 1.3 and      # Reasonable aspect ratio
            std_intensity > 30                # Good contrast (high standard deviation)
        )
        
        return is_fingerprint, {
            'edge_density': float(edge_density),
            'texture_score': float(texture_score),
            'mean_intensity': float(mean_intensity),
            'std_intensity': float(std_intensity),
            'mid_freq_energy': float(mid_freq_energy),
            'aspect_ratio': float(aspect_ratio)
        }
        
    except Exception as e:
        print(f"Error in fingerprint validation: {e}")
        return False, {}

@app.route('/predict', methods=['POST', 'OPTIONS'])
# Apply cross_origin decorator for CORS handling
@cross_origin(origin='http://localhost:5173', headers=['Content-Type'])
def predict():
    # Handle preflight requests for CORS
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    try:
        # Check if the 'image' file is present in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        # Get the image file from the request
        image = request.files['image']
        # Check if the file is empty
        if image.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Open the image using Pillow
        img = Image.open(image)

        # Convert RGBA to RGB if necessary, as most models expect 3 channels
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize the image to the target size expected by the ResNet model
        # The notebook uses (256, 256), so we'll use that here.
        img = img.resize((256, 256))

        # Convert the image to a numpy array
        img_array = np.array(img)

        # Check if the image is likely a fingerprint
        is_fingerprint, validation_metrics = is_likely_fingerprint(img_array)
        
        if not is_fingerprint:
            return jsonify({
                'error': 'The uploaded image does not appear to be a fingerprint. Please upload a clear fingerprint image.',
                'validation_metrics': validation_metrics
            }), 400

        # Add a batch dimension to the array (shape becomes (1, 256, 256, 3))
        # This is required because models expect input in batches
        img_array = np.expand_dims(img_array, axis=0)

        # Apply the correct preprocessing for the ResNet50 model
        # This function scales pixel values and performs centering based on ImageNet statistics
        img_array = preprocess_input(img_array)

        # Make prediction using the loaded model
        prediction = model.predict(img_array)
        # Get the index of the class with the highest probability
        predicted_class = np.argmax(prediction, axis=1)[0]
        # Get the confidence score for the predicted class
        confidence = float(prediction[0][predicted_class])

        # Get the blood group label using the predicted class index
        # Ensure the labels dictionary is correctly defined
        blood_group = labels[predicted_class]

        # --- Log prediction for stats ---
        prediction_stats['total'] += 1
        prediction_stats['blood_groups'][blood_group] = prediction_stats['blood_groups'].get(blood_group, 0) + 1
        prediction_stats['confidences'].append(confidence)
        # Add to recent predictions (keep only last 50)
        prediction_stats['recent_predictions'].append({
            'blood_group': blood_group,
            'confidence': confidence,
            'timestamp': datetime.datetime.now().isoformat()
        })
        if len(prediction_stats['recent_predictions']) > 50:
            prediction_stats['recent_predictions'] = prediction_stats['recent_predictions'][-50:]

        # Generate Grad-CAM visualization
        overlay, heatmap = generate_gradcam(model, img_array, predicted_class)

        # Encode overlay and heatmap to base64
        overlay_base64 = encode_image_to_base64(overlay) if overlay is not None else None
        heatmap_base64 = encode_image_to_base64(heatmap) if heatmap is not None else None

        # Return the prediction results as a JSON response
        return jsonify({
            'blood_group': blood_group,
            'confidence': confidence,
            'validation_metrics': validation_metrics,
            'overlay': overlay_base64,
            'heatmap': heatmap_base64,
            'xai_available': overlay_base64 is not None and heatmap_base64 is not None
        })

    except Exception as e:
        # Catch any potential errors during the process and return an error response
        return jsonify({'error': str(e)}), 500

# --- Stats endpoint for dashboard ---
@app.route('/stats', methods=['GET'])
@cross_origin(origin='http://localhost:5173', headers=['Content-Type'])
def stats():
    # Return a snapshot of the stats
    return jsonify({
        'total': prediction_stats['total'],
        'blood_groups': prediction_stats['blood_groups'],
        'confidences': prediction_stats['confidences'],
        'recent_predictions': prediction_stats['recent_predictions']
    })

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
