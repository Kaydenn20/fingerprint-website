#!/usr/bin/env python3
"""
Quick script to upload model to Firebase Hosting
"""

import os
import shutil
from pathlib import Path

def setup_firebase_hosting():
    """Set up Firebase hosting for model files"""
    
    # Create public directory if it doesn't exist
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    
    # Create models subdirectory
    models_dir = public_dir / "models"
    models_dir.mkdir(exist_ok=True)
    
    # Copy model file to public directory
    model_source = Path("backend/model.resnet.keras")
    model_dest = models_dir / "model.resnet.keras"
    
    if model_source.exists():
        shutil.copy2(model_source, model_dest)
        print(f"✓ Model copied to {model_dest}")
        print(f"✓ Firebase hosting ready!")
        print("\nNext steps:")
        print("1. Run: firebase deploy --only hosting")
        print("2. Update MODEL_URL in backend/main.py with your Firebase URL")
        print("3. Start your backend: python backend/main.py")
    else:
        print("❌ Model file not found at backend/model.resnet.keras")
        print("Please ensure your model file exists before running this script.")

if __name__ == "__main__":
    setup_firebase_hosting() 