#!/usr/bin/env python3
"""
Two-Stage Model Training Script
Stage 1: Fingerprint vs Non-Fingerprint Classification
Stage 2: Blood Group Classification (only for confirmed fingerprints)
"""

import os
import shutil
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model_architecture import (
    create_fingerprint_classifier,
    create_blood_group_classifier,
    train_fingerprint_classifier,
    train_blood_group_classifier
)

def create_dataset_structure(base_path="datasets"):
    """
    Create the dataset directory structure
    """
    structure = {
        'fingerprint_classifier': {
            'train': ['fingerprint', 'non_fingerprint'],
            'validation': ['fingerprint', 'non_fingerprint']
        },
        'blood_group_classifier': {
            'train': ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-'],
            'validation': ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
        }
    }
    
    for model_type, splits in structure.items():
        for split, classes in splits.items():
            for class_name in classes:
                path = os.path.join(base_path, model_type, split, class_name)
                os.makedirs(path, exist_ok=True)
                print(f"Created: {path}")
    
    return structure

def prepare_fingerprint_dataset(
    fingerprint_images_dir,
    non_fingerprint_images_dir,
    output_dir="datasets/fingerprint_classifier",
    train_split=0.8
):
    """
    Prepare dataset for fingerprint classifier
    """
    print("📁 Preparing Fingerprint Classification Dataset...")
    
    # Create directories
    train_fingerprint = os.path.join(output_dir, "train", "fingerprint")
    train_non_fingerprint = os.path.join(output_dir, "train", "non_fingerprint")
    val_fingerprint = os.path.join(output_dir, "validation", "fingerprint")
    val_non_fingerprint = os.path.join(output_dir, "validation", "non_fingerprint")
    
    os.makedirs(train_fingerprint, exist_ok=True)
    os.makedirs(train_non_fingerprint, exist_ok=True)
    os.makedirs(val_fingerprint, exist_ok=True)
    os.makedirs(val_non_fingerprint, exist_ok=True)
    
    # Process fingerprint images
    if os.path.exists(fingerprint_images_dir):
        fingerprint_files = [f for f in os.listdir(fingerprint_images_dir) 
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Split into train/validation
        np.random.shuffle(fingerprint_files)
        split_idx = int(len(fingerprint_files) * train_split)
        
        train_files = fingerprint_files[:split_idx]
        val_files = fingerprint_files[split_idx:]
        
        # Copy files
        for file in train_files:
            src = os.path.join(fingerprint_images_dir, file)
            dst = os.path.join(train_fingerprint, file)
            shutil.copy2(src, dst)
        
        for file in val_files:
            src = os.path.join(fingerprint_images_dir, file)
            dst = os.path.join(val_fingerprint, file)
            shutil.copy2(src, dst)
        
        print(f"   ✅ Fingerprint images: {len(train_files)} train, {len(val_files)} validation")
    
    # Process non-fingerprint images
    if os.path.exists(non_fingerprint_images_dir):
        non_fingerprint_files = [f for f in os.listdir(non_fingerprint_images_dir) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Split into train/validation
        np.random.shuffle(non_fingerprint_files)
        split_idx = int(len(non_fingerprint_files) * train_split)
        
        train_files = non_fingerprint_files[:split_idx]
        val_files = non_fingerprint_files[split_idx:]
        
        # Copy files
        for file in train_files:
            src = os.path.join(non_fingerprint_images_dir, file)
            dst = os.path.join(train_non_fingerprint, file)
            shutil.copy2(src, dst)
        
        for file in val_files:
            src = os.path.join(non_fingerprint_images_dir, file)
            dst = os.path.join(val_non_fingerprint, file)
            shutil.copy2(src, dst)
        
        print(f"   ✅ Non-fingerprint images: {len(train_files)} train, {len(val_files)} validation")

def prepare_blood_group_dataset(
    blood_group_images_dir,
    output_dir="datasets/blood_group_classifier",
    train_split=0.8
):
    """
    Prepare dataset for blood group classifier
    """
    print("📁 Preparing Blood Group Classification Dataset...")
    
    blood_groups = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
    
    for blood_group in blood_groups:
        # Create directories
        train_dir = os.path.join(output_dir, "train", blood_group)
        val_dir = os.path.join(output_dir, "validation", blood_group)
        
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)
        
        # Source directory for this blood group
        src_dir = os.path.join(blood_group_images_dir, blood_group)
        
        if os.path.exists(src_dir):
            files = [f for f in os.listdir(src_dir) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Split into train/validation
            np.random.shuffle(files)
            split_idx = int(len(files) * train_split)
            
            train_files = files[:split_idx]
            val_files = files[split_idx:]
            
            # Copy files
            for file in train_files:
                src = os.path.join(src_dir, file)
                dst = os.path.join(train_dir, file)
                shutil.copy2(src, dst)
            
            for file in val_files:
                src = os.path.join(src_dir, file)
                dst = os.path.join(val_dir, file)
                shutil.copy2(src, dst)
            
            print(f"   ✅ {blood_group}: {len(train_files)} train, {len(val_files)} validation")

def train_models():
    """
    Train both models
    """
    print("🚀 Starting Two-Stage Model Training...")
    
    # Train Stage 1: Fingerprint Classifier
    print("\n" + "="*60)
    print("STAGE 1: Training Fingerprint Classifier")
    print("="*60)
    
    fingerprint_train_dir = "datasets/fingerprint_classifier/train"
    fingerprint_val_dir = "datasets/fingerprint_classifier/validation"
    
    if os.path.exists(fingerprint_train_dir) and os.path.exists(fingerprint_val_dir):
        print("Training fingerprint classifier...")
        fingerprint_model, fingerprint_history = train_fingerprint_classifier(
            fingerprint_train_dir,
            fingerprint_val_dir,
            epochs=20,
            batch_size=32
        )
        print("✅ Fingerprint classifier trained and saved!")
    else:
        print("❌ Fingerprint dataset not found. Please prepare the dataset first.")
    
    # Train Stage 2: Blood Group Classifier
    print("\n" + "="*60)
    print("STAGE 2: Training Blood Group Classifier")
    print("="*60)
    
    blood_group_train_dir = "datasets/blood_group_classifier/train"
    blood_group_val_dir = "datasets/blood_group_classifier/validation"
    
    if os.path.exists(blood_group_train_dir) and os.path.exists(blood_group_val_dir):
        print("Training blood group classifier...")
        blood_group_model, blood_group_history = train_blood_group_classifier(
            blood_group_train_dir,
            blood_group_val_dir,
            epochs=30,
            batch_size=32
        )
        print("✅ Blood group classifier trained and saved!")
    else:
        print("❌ Blood group dataset not found. Please prepare the dataset first.")

def main():
    """
    Main training pipeline
    """
    print("🏥 Two-Stage Fingerprint Classification System")
    print("=" * 60)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Create dataset structure
    print("\n1. Creating dataset structure...")
    create_dataset_structure()
    
    # Prepare datasets (uncomment and modify paths as needed)
    print("\n2. Preparing datasets...")
    print("   ⚠️  Please uncomment and modify the dataset preparation calls below")
    print("   with your actual image directories.")
    
    # Example dataset preparation (uncomment and modify paths):
    # prepare_fingerprint_dataset(
    #     fingerprint_images_dir="path/to/fingerprint/images",
    #     non_fingerprint_images_dir="path/to/non_fingerprint/images"
    # )
    # 
    # prepare_blood_group_dataset(
    #     blood_group_images_dir="path/to/blood_group/images"
    # )
    
    # Train models
    print("\n3. Training models...")
    train_models()
    
    print("\n" + "="*60)
    print("✅ Training completed!")
    print("="*60)
    print("\nSaved models:")
    print("   - fingerprint_classifier.keras")
    print("   - blood_group_classifier.keras")
    print("\nNext steps:")
    print("   1. Update main.py to use the two-stage system")
    print("   2. Test with real images")
    print("   3. Deploy the improved system")

if __name__ == "__main__":
    main() 