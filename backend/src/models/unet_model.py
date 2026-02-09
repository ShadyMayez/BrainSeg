"""
U-Net Model for Brain Tumor Segmentation
========================================
U-Net with EfficientNetB0 backbone as specified in the notebook.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Then use keras directly
K = keras.backend
Model = keras.models.Model
from keras.layers import Input, Conv2D, Dropout, BatchNormalization, UpSampling2D, concatenate
from keras.applications import EfficientNetB0
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def weighted_dice_loss(y_true, y_pred, class_weights=None):
    """Weighted Dice Loss for imbalanced classes."""
    if class_weights is None:
        class_weights = np.array([0.45, 0.25, 0.20, 0.20])
    
    smooth = 1e-6
    y_true = K.cast(y_true, 'float32')
    y_pred = K.cast(y_pred, 'float32')
    
    intersection = K.sum(y_true * y_pred, axis=[1, 2])
    union = K.sum(y_true + y_pred, axis=[1, 2])
    
    dice = (2.0 * intersection + smooth) / (union + smooth)
    weighted_dice = -K.sum(class_weights * dice, axis=-1)
    return K.mean(weighted_dice)


def dice_coef(y_true, y_pred, smooth=1.0):
    """Dice coefficient metric."""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    intersection = K.sum(y_true * y_pred, axis=(1, 2, 3))
    return K.mean(
        (2. * intersection + smooth) / 
        (K.sum(y_true, axis=(1, 2, 3)) + K.sum(y_pred, axis=(1, 2, 3)) + smooth)
    )


def dice_coef_necrotic(y_true, y_pred, epsilon=1e-6):
    """Dice coefficient for Necrotic/Core class."""
    y_true = K.cast(y_true, y_pred.dtype)
    y_true_necrotic = y_true[..., 1]
    y_pred_necrotic = y_pred[..., 1]
    intersection = K.sum(K.abs(y_true_necrotic * y_pred_necrotic))
    return (2. * intersection) / (
        K.sum(K.square(y_true_necrotic)) + K.sum(K.square(y_pred_necrotic)) + epsilon
    )


def dice_coef_edema(y_true, y_pred, epsilon=1e-6):
    """Dice coefficient for Edema class."""
    y_true = K.cast(y_true, y_pred.dtype)
    y_true_edema = y_true[..., 2]
    y_pred_edema = y_pred[..., 2]
    intersection = K.sum(K.abs(y_true_edema * y_pred_edema))
    return (2. * intersection) / (
        K.sum(K.square(y_true_edema)) + K.sum(K.square(y_pred_edema)) + epsilon
    )


def dice_coef_enhancing(y_true, y_pred, epsilon=1e-6):
    """Dice coefficient for Enhancing Tumor class."""
    y_true = K.cast(y_true, y_pred.dtype)
    y_true_enhancing = y_true[..., 3]
    y_pred_enhancing = y_pred[..., 3]
    intersection = K.sum(K.abs(y_true_enhancing * y_pred_enhancing))
    return (2. * intersection) / (
        K.sum(K.square(y_true_enhancing)) + K.sum(K.square(y_pred_enhancing)) + epsilon
    )


def precision(y_true, y_pred):
    """Precision metric."""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    return true_positives / (predicted_positives + K.epsilon())


def sensitivity(y_true, y_pred):
    """Sensitivity (Recall) metric."""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())


def specificity(y_true, y_pred):
    """Specificity metric."""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    true_negatives = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
    possible_negatives = K.sum(K.round(K.clip(1 - y_true, 0, 1)))
    return true_negatives / (possible_negatives + K.epsilon())


def build_unet(input_shape=(128, 128, 3), num_classes=4):
    """
    Build U-Net model with EfficientNetB0 backbone.
    Exact architecture from notebook.
    
    Args:
        input_shape: Input image shape (H, W, C)
        num_classes: Number of segmentation classes
    
    Returns:
        Keras Model
    """
    inputs = Input(input_shape)
    
    # Encoder: Using EfficientNetB0 as Backbone
    base_model = EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_tensor=inputs
    )
    
    # Extract Encoder Outputs for Skip Connections
    skip1 = base_model.get_layer('block2a_expand_activation').output  # 64x64
    skip2 = base_model.get_layer('block3a_expand_activation').output  # 32x32
    skip3 = base_model.get_layer('block4a_expand_activation').output  # 16x16
    skip4 = base_model.get_layer('block6a_expand_activation').output  # 8x8
    
    # Bottleneck
    x = base_model.output  # 4x4
    
    # Decoder: Manually Implemented Layers
    # 1st Decoder Block
    x = UpSampling2D()(x)
    x = concatenate([x, skip4])
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    
    # 2nd Decoder Block
    x = UpSampling2D()(x)
    x = concatenate([x, skip3])
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    
    # 3rd Decoder Block
    x = UpSampling2D()(x)
    x = concatenate([x, skip2])
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    
    # 4th Decoder Block
    x = UpSampling2D()(x)
    x = concatenate([x, skip1])
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    
    # Final Upsampling to Match Input Resolution
    x = UpSampling2D()(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    
    # Output Layer
    outputs = Conv2D(num_classes, (1, 1), activation='softmax')(x)
    
    # Define the Model
    model = Model(inputs=[inputs], outputs=[outputs])
    return model


def compile_model(model, class_weights=None):
    """Compile model with weighted dice loss."""
    if class_weights is None:
        class_weights = np.array([0.45, 0.25, 0.20, 0.20])
    
    model.compile(
        optimizer='adam',
        loss=lambda y_true, y_pred: weighted_dice_loss(y_true, y_pred, class_weights),
        metrics=[
            'accuracy',
            dice_coef,
            dice_coef_necrotic,
            dice_coef_edema,
            dice_coef_enhancing,
            precision,
            sensitivity,
            specificity
        ]
    )
    return model


class BrainTumorSegmenter:
    """Inference wrapper for brain tumor segmentation model."""
    
    CLASS_LABELS = {
        0: 'Non-tumor',
        1: 'Necrotic/Core',
        2: 'Edema',
        3: 'Enhancing Tumor'
    }
    
    CLASS_COLORS = {
        0: [0, 0, 0],
        1: [0, 0, 255],
        2: [255, 192, 203],
        3: [0, 255, 255]
    }
    
    _instance = None
    _model = None
    
    def __new__(cls, model_path: str = None):
        """Singleton pattern for model loading."""
        if cls._instance is None:
            cls._instance = super(BrainTumorSegmenter, cls).__new__(cls)
            cls._instance.model_path = model_path
            cls._instance.model = None
            if model_path and os.path.exists(model_path):
                cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load model from path."""
        try:
            class_weights = np.array([0.45, 0.25, 0.20, 0.20])
            custom_objects = {
                'weighted_dice_loss': lambda y_true, y_pred: weighted_dice_loss(y_true, y_pred, class_weights),
                'dice_coef': dice_coef,
                'dice_coef_necrotic': dice_coef_necrotic,
                'dice_coef_edema': dice_coef_edema,
                'dice_coef_enhancing': dice_coef_enhancing,
                'precision': precision,
                'sensitivity': sensitivity,
                'specificity': specificity
            }
            
            self.model = tf.keras.models.load_model(
                self.model_path,
                safe_mode=False,
                custom_objects=custom_objects
            )
            logger.info(f"Model loaded from {self.model_path}")
        except Exception:
            logger.exception(f"Failed to load model from {self.model_path}")
            self.model = None
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Predict segmentation mask.
        
        Args:
            image: Input image (1, 128, 128, 3) or (128, 128, 3)
        
        Returns:
            Segmentation mask (128, 128, 4) - one-hot encoded
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Add batch dimension if needed
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Predict
        pred = self.model.predict(image, verbose=0)
        return pred[0]
    
    def predict_class_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Predict class mask (argmax).
        
        Args:
            image: Input image
        
        Returns:
            Class mask (128, 128) with values 0-3
        """
        pred = self.predict(image)
        class_mask = np.argmax(pred, axis=-1)
        return class_mask
    
    def get_tumor_regions(self, class_mask: np.ndarray) -> dict:
        """
        Get tumor region statistics.
        
        Args:
            class_mask: Predicted class mask
        
        Returns:
            Dictionary with region statistics
        """
        total_pixels = class_mask.size
        stats = {}
        
        for class_idx, label in self.CLASS_LABELS.items():
            pixel_count = int(np.sum(class_mask == class_idx))
            percentage = float((pixel_count / total_pixels) * 100)
            stats[label] = {
                'pixel_count': pixel_count,
                'percentage': round(percentage, 2)
            }
        
        return stats


def get_segmenter(model_path: str = None) -> BrainTumorSegmenter:
    """Get or create segmenter singleton."""
    return BrainTumorSegmenter(model_path)
