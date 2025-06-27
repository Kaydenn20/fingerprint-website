#!/usr/bin/env python3
"""
Test script for fingerprint validation
"""

import cv2
import numpy as np
from PIL import Image
import requests
import json

def is_likely_fingerprint(image_array):
    """
    Simple heuristic to check if an image is likely a fingerprint
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
        
        # Fingerprint characteristics:
        # 1. Moderate to high edge density (ridges and valleys)
        # 2. High texture variance (detailed patterns)
        # 3. Moderate intensity (not too bright or dark)
        
        is_fingerprint = (
            edge_density > 0.05 and  # At least 5% of pixels are edges
            texture_score > 500 and  # High texture variance
            50 < mean_intensity < 200  # Moderate brightness
        )
        
        return is_fingerprint, {
            'edge_density': edge_density,
            'texture_score': texture_score,
            'mean_intensity': mean_intensity,
            'std_intensity': std_intensity
        }
        
    except Exception as e:
        print(f"Error in fingerprint validation: {e}")
        return False, {}

def test_validation():
    """Test the validation function with different image types"""
    
    print("🧪 Testing Fingerprint Validation")
    print("=" * 50)
    
    # Test 1: Create a simple fingerprint-like pattern
    print("\n1. Testing with fingerprint-like pattern...")
    fingerprint_pattern = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
    # Add some ridge-like patterns
    for i in range(0, 256, 4):
        fingerprint_pattern[:, i:i+2] = 100
    fingerprint_pattern[:, 100:102] = 150
    
    is_fp, metrics = is_likely_fingerprint(fingerprint_pattern)
    print(f"   Result: {'✅ Fingerprint detected' if is_fp else '❌ Not a fingerprint'}")
    print(f"   Edge density: {metrics.get('edge_density', 0):.4f}")
    print(f"   Texture score: {metrics.get('texture_score', 0):.2f}")
    print(f"   Mean intensity: {metrics.get('mean_intensity', 0):.2f}")
    
    # Test 2: Create a plain image (should fail)
    print("\n2. Testing with plain image...")
    plain_image = np.full((256, 256, 3), 128, dtype=np.uint8)
    
    is_fp, metrics = is_likely_fingerprint(plain_image)
    print(f"   Result: {'✅ Fingerprint detected' if is_fp else '❌ Not a fingerprint'}")
    print(f"   Edge density: {metrics.get('edge_density', 0):.4f}")
    print(f"   Texture score: {metrics.get('texture_score', 0):.2f}")
    print(f"   Mean intensity: {metrics.get('mean_intensity', 0):.2f}")
    
    # Test 3: Create a high-contrast image (should fail)
    print("\n3. Testing with high-contrast image...")
    high_contrast = np.zeros((256, 256, 3), dtype=np.uint8)
    high_contrast[::2, ::2] = 255
    
    is_fp, metrics = is_likely_fingerprint(high_contrast)
    print(f"   Result: {'✅ Fingerprint detected' if is_fp else '❌ Not a fingerprint'}")
    print(f"   Edge density: {metrics.get('edge_density', 0):.4f}")
    print(f"   Texture score: {metrics.get('texture_score', 0):.2f}")
    print(f"   Mean intensity: {metrics.get('mean_intensity', 0):.2f}")
    
    print("\n" + "=" * 50)
    print("✅ Validation test completed!")

def test_api_endpoint():
    """Test the API endpoint with different images"""
    
    print("\n🌐 Testing API Endpoint")
    print("=" * 50)
    
    # Create test images
    test_images = {
        "fingerprint_like": np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8),
        "plain": np.full((256, 256, 3), 128, dtype=np.uint8),
        "high_contrast": np.zeros((256, 256, 3), dtype=np.uint8)
    }
    
    # Add fingerprint-like patterns
    for i in range(0, 256, 4):
        test_images["fingerprint_like"][:, i:i+2] = 100
    test_images["fingerprint_like"][:, 100:102] = 150
    
    # Add high contrast pattern
    test_images["high_contrast"][::2, ::2] = 255
    
    for name, img_array in test_images.items():
        print(f"\nTesting {name} image...")
        
        # Convert to PIL Image and save temporarily
        img = Image.fromarray(img_array)
        img.save(f"test_{name}.png")
        
        try:
            # Send to API
            with open(f"test_{name}.png", "rb") as f:
                files = {"image": f}
                response = requests.post("http://localhost:5000/predict", files=files)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('blood_group', 'Unknown')} (confidence: {data.get('confidence', 0):.2f})")
            else:
                data = response.json()
                print(f"   ❌ Rejected: {data.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Clean up
        import os
        if os.path.exists(f"test_{name}.png"):
            os.remove(f"test_{name}.png")

if __name__ == "__main__":
    test_validation()
    test_api_endpoint() 