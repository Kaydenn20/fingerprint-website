"""
Model Architecture for Two-Stage Fingerprint Classification System
Stage 1: Fingerprint vs Non-Fingerprint (Binary Classification)
Stage 2: Blood Group Classification (8 classes)
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

def create_fingerprint_classifier(input_shape=(256, 256, 3)):
    """
    Create a binary classifier to distinguish fingerprints from non-fingerprints
    """
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1, activation='sigmoid', name='fingerprint_probability')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall']
    )
    
    return model

def create_blood_group_classifier(input_shape=(256, 256, 3)):
    """
    Create a blood group classifier (8 classes: A+, A-, AB+, AB-, B+, B-, O+, O-)
    """
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze the base model layers
    base_model.trainable = False
    
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(8, activation='softmax', name='blood_group_probability')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def prepare_dataset_structure():
    """
    Create the recommended dataset structure for training
    """
    dataset_structure = {
        'fingerprint_classifier': {
            'train': {
                'fingerprint': 'path/to/fingerprint_classifier/train/fingerprint/',
                'non_fingerprint': 'path/to/fingerprint_classifier/train/non_fingerprint/'
            },
            'validation': {
                'fingerprint': 'path/to/fingerprint_classifier/validation/fingerprint/',
                'non_fingerprint': 'path/to/fingerprint_classifier/validation/non_fingerprint/'
            }
        },
        'blood_group_classifier': {
            'train': {
                'A+': 'path/to/blood_group_classifier/train/A+/',
                'A-': 'path/to/blood_group_classifier/train/A-/',
                'AB+': 'path/to/blood_group_classifier/train/AB+/',
                'AB-': 'path/to/blood_group_classifier/train/AB-/',
                'B+': 'path/to/blood_group_classifier/train/B+/',
                'B-': 'path/to/blood_group_classifier/train/B-/',
                'O+': 'path/to/blood_group_classifier/train/O+/',
                'O-': 'path/to/blood_group_classifier/train/O-/'
            },
            'validation': {
                'A+': 'path/to/blood_group_classifier/validation/A+/',
                'A-': 'path/to/blood_group_classifier/validation/A-/',
                'AB+': 'path/to/blood_group_classifier/validation/AB+/',
                'AB-': 'path/to/blood_group_classifier/validation/AB-/',
                'B+': 'path/to/blood_group_classifier/validation/B+/',
                'B-': 'path/to/blood_group_classifier/validation/B-/',
                'O+': 'path/to/blood_group_classifier/validation/O+/',
                'O-': 'path/to/blood_group_classifier/validation/O-/'
            }
        }
    }
    
    return dataset_structure

def create_data_generators():
    """
    Create data generators for both models
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    return train_datagen, val_datagen

def train_fingerprint_classifier(train_dir, val_dir, epochs=20, batch_size=32):
    """
    Train the fingerprint classifier
    """
    train_datagen, val_datagen = create_data_generators()
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='binary',
        classes=['non_fingerprint', 'fingerprint']
    )
    
    # Load validation data
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='binary',
        classes=['non_fingerprint', 'fingerprint']
    )
    
    # Create and train model
    model = create_fingerprint_classifier()
    
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=val_generator.samples // batch_size
    )
    
    # Save the model
    model.save('fingerprint_classifier.keras')
    
    return model, history

def train_blood_group_classifier(train_dir, val_dir, epochs=30, batch_size=32):
    """
    Train the blood group classifier
    """
    train_datagen, val_datagen = create_data_generators()
    
    # Load training data
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    # Load validation data
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(256, 256),
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    # Create and train model
    model = create_blood_group_classifier()
    
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=val_generator.samples // batch_size
    )
    
    # Save the model
    model.save('blood_group_classifier.keras')
    
    return model, history

if __name__ == "__main__":
    print("Model Architecture Definitions")
    print("=" * 50)
    print("\n1. Fingerprint Classifier (Binary)")
    print("   - Input: 256x256x3 images")
    print("   - Output: 1 (fingerprint probability)")
    print("   - Classes: [non_fingerprint, fingerprint]")
    
    print("\n2. Blood Group Classifier (Multi-class)")
    print("   - Input: 256x256x3 images")
    print("   - Output: 8 (blood group probabilities)")
    print("   - Classes: [A+, A-, AB+, AB-, B+, B-, O+, O-]")
    
    print("\n3. Dataset Structure")
    structure = prepare_dataset_structure()
    for model_type, splits in structure.items():
        print(f"\n   {model_type}:")
        for split, classes in splits.items():
            print(f"     {split}: {list(classes.keys())}")
    
    print("\n✅ Model architectures ready for training!") 