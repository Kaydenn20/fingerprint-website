#!/usr/bin/env python3
"""
Test script for strict fingerprint detection
"""

import requests
import json
import os
import time

def test_strict_fingerprint_detection():
    """Test the strict fingerprint detection system"""
    print("🔍 Testing Strict Fingerprint Detection System")
    print("=" * 60)
    
    # API endpoint
    url = "http://localhost:5000/predict"
    
    # Test cases
    test_cases = [
        {
            "name": "Fingerprint Image (A+)",
            "path": "dataset/dataset_blood_group/A+/cluster_0_1001.BMP",
            "expected_fingerprint": True,
            "expected_blood_group": "A+"
        },
        {
            "name": "Fingerprint Image (B+)",
            "path": "dataset/dataset_blood_group/B+/cluster_0_1001.BMP",
            "expected_fingerprint": True,
            "expected_blood_group": "B+"
        },
        {
            "name": "Non-Fingerprint Image",
            "path": "dataset_non_fingerprint/non_fingerprint_1.jpg",
            "expected_fingerprint": False,
            "expected_blood_group": None
        }
    ]
    
    print("🧪 Running test cases...")
    print("-" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        
        # Check if test file exists
        if not os.path.exists(test_case['path']):
            print(f"   ❌ Test file not found: {test_case['path']}")
            continue
        
        try:
            # Prepare the image file
            with open(test_case['path'], 'rb') as f:
                files = {'image': f}
                
                # Make API request
                response = requests.post(url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract results
                    blood_group = result.get('blood_group', None)
                    confidence = result.get('confidence', 0.0)
                    validation_metrics = result.get('validation_metrics', {})
                    
                    # If we got a blood_group, it means fingerprint was detected
                    is_fingerprint = blood_group is not None
                    
                    # Check if result matches expectation
                    fingerprint_success = is_fingerprint == test_case['expected_fingerprint']
                    blood_group_success = True
                    
                    if is_fingerprint and test_case['expected_blood_group']:
                        blood_group_success = blood_group == test_case['expected_blood_group']
                    
                    print(f"   📊 Fingerprint Detected: {'✅ YES' if is_fingerprint else '❌ NO'}")
                    print(f"   🎯 Expected Fingerprint: {'✅ YES' if test_case['expected_fingerprint'] else '❌ NO'}")
                    
                    if is_fingerprint:
                        print(f"   🩸 Blood Group: {blood_group}")
                        print(f"   📈 Confidence: {confidence:.3f}")
                        print(f"   🎯 Expected Blood Group: {test_case['expected_blood_group']}")
                    
                    # Show validation metrics
                    print(f"   📊 Validation Metrics:")
                    for key, value in validation_metrics.items():
                        print(f"      {key}: {value:.3f}")
                    
                    print(f"   {'✅ PASS' if fingerprint_success and blood_group_success else '❌ FAIL'}")
                    
                elif response.status_code == 400:
                    result = response.json()
                    error = result.get('error', '')
                    validation_metrics = result.get('validation_metrics', {})
                    
                    # If we got a 400 error, it means fingerprint was rejected
                    is_fingerprint = False
                    fingerprint_success = is_fingerprint == test_case['expected_fingerprint']
                    
                    print(f"   📊 Fingerprint Detected: ❌ NO (Rejected)")
                    print(f"   🎯 Expected Fingerprint: {'✅ YES' if test_case['expected_fingerprint'] else '❌ NO'}")
                    print(f"   💬 Error: {error}")
                    
                    # Show validation metrics
                    print(f"   📊 Validation Metrics:")
                    for key, value in validation_metrics.items():
                        print(f"      {key}: {value:.3f}")
                    
                    print(f"   {'✅ PASS' if fingerprint_success else '❌ FAIL'}")
                    
                else:
                    print(f"   ❌ API Error: {response.status_code}")
                    print(f"   📄 Response: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Test Error: {str(e)}")
        
        print("-" * 60)
    
    print("=" * 60)
    print("🎯 Strict Fingerprint Detection Test Complete!")

if __name__ == "__main__":
    test_strict_fingerprint_detection() 