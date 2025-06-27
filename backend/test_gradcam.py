#!/usr/bin/env python3
"""
Test script for Grad-CAM functionality
This script tests the Grad-CAM implementation to ensure it works correctly
"""

import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os

def test_gradcam():
    """Test the Grad-CAM functionality"""
    
    print("🧬 Testing Grad-CAM Functionality...")
    
    # Check if model exists
    model_path = "model.resnet.keras"
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False
    
    try:
        # Load the model
        print("📥 Loading model...")
        model = load_model(model_path)
        print("✅ Model loaded successfully")
        
        # Create a test image (random noise for testing)
        print("🖼️ Creating test image...")
        test_image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        
        # Preprocess the image
        img_array = np.expand_dims(test_image, axis=0)
        img_array = preprocess_input(img_array)
        
        # Make prediction
        print("🔮 Making prediction...")
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence = float(prediction[0][predicted_class])
        
        print(f"✅ Prediction: Class {predicted_class}, Confidence: {confidence:.4f}")
        
        # Test Grad-CAM function
        print("🔍 Testing Grad-CAM generation...")
        from main import generate_gradcam, encode_image_to_base64
        
        overlay, heatmap = generate_gradcam(model, img_array, predicted_class)
        
        if overlay is not None and heatmap is not None:
            print("✅ Grad-CAM generated successfully")
            
            # Test encoding
            print("📤 Testing image encoding...")
            overlay_base64 = encode_image_to_base64(overlay)
            heatmap_base64 = encode_image_to_base64(heatmap)
            
            if overlay_base64 and heatmap_base64:
                print("✅ Image encoding successful")
                print(f"📊 Overlay size: {len(overlay_base64)} characters")
                print(f"📊 Heatmap size: {len(heatmap_base64)} characters")
                return True
            else:
                print("❌ Image encoding failed")
                return False
        else:
            print("❌ Grad-CAM generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_gradcam()
    if success:
        print("\n🎉 All tests passed! Grad-CAM is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the implementation.") 