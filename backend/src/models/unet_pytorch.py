"""
PyTorch U-Net Model for Brain Tumor Segmentation
================================================
Based on the Kaggle notebook architecture.
4-channel input (flair, t1, t1ce, t2)
"""

import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UNet(nn.Module):
    """U-Net architecture matching the Kaggle notebook."""
    
    def __init__(self, in_channels=2, num_classes=4, dropout=0.5):
        super(UNet, self).__init__()
        
        # Encoder (Contracting Path)
        # Block 1
        self.conv1_1 = nn.Conv2d(in_channels, 32, kernel_size=3, padding=1)
        self.conv1_2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Block 2
        self.conv2_1 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv2_2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Block 3
        self.conv3_1 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3_2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Block 4
        self.conv4_1 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv4_2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Block 5 (Bottleneck)
        self.conv5_1 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.conv5_2 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.dropout = nn.Dropout2d(p=dropout)
        
        # Decoder (Expanding Path)
        # Block 6
        self.upconv6 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.conv6_1 = nn.Conv2d(512, 256, kernel_size=3, padding=1)
        self.conv6_2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        
        # Block 7
        self.upconv7 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv7_1 = nn.Conv2d(256, 128, kernel_size=3, padding=1)
        self.conv7_2 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        
        # Block 8
        self.upconv8 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv8_1 = nn.Conv2d(128, 64, kernel_size=3, padding=1)
        self.conv8_2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        
        # Block 9
        self.upconv9 = nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2)
        self.conv9_1 = nn.Conv2d(64, 32, kernel_size=3, padding=1)
        self.conv9_2 = nn.Conv2d(32, 32, kernel_size=3, padding=1)
        
        # Output layer
        self.conv10 = nn.Conv2d(32, num_classes, kernel_size=1)
        
        self._initialize_weights()
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        # Encoder
        conv1 = F.relu(self.conv1_1(x))
        conv1 = F.relu(self.conv1_2(conv1))
        pool1 = self.pool1(conv1)
        
        conv2 = F.relu(self.conv2_1(pool1))
        conv2 = F.relu(self.conv2_2(conv2))
        pool2 = self.pool2(conv2)
        
        conv3 = F.relu(self.conv3_1(pool2))
        conv3 = F.relu(self.conv3_2(conv3))
        pool3 = self.pool3(conv3)
        
        conv4 = F.relu(self.conv4_1(pool3))
        conv4 = F.relu(self.conv4_2(conv4))
        pool4 = self.pool4(conv4)
        
        conv5 = F.relu(self.conv5_1(pool4))
        conv5 = F.relu(self.conv5_2(conv5))
        conv5 = self.dropout(conv5)
        
        # Decoder
        up6 = self.upconv6(conv5)
        merge6 = torch.cat([conv4, up6], dim=1)
        conv6 = F.relu(self.conv6_1(merge6))
        conv6 = F.relu(self.conv6_2(conv6))
        
        up7 = self.upconv7(conv6)
        merge7 = torch.cat([conv3, up7], dim=1)
        conv7 = F.relu(self.conv7_1(merge7))
        conv7 = F.relu(self.conv7_2(conv7))
        
        up8 = self.upconv8(conv7)
        merge8 = torch.cat([conv2, up8], dim=1)
        conv8 = F.relu(self.conv8_1(merge8))
        conv8 = F.relu(self.conv8_2(conv8))
        
        up9 = self.upconv9(conv8)
        merge9 = torch.cat([conv1, up9], dim=1)
        conv9 = F.relu(self.conv9_1(merge9))
        conv9 = F.relu(self.conv9_2(conv9))
        
        out = self.conv10(conv9)
        return out


class BrainTumorSegmenter:
    """PyTorch inference wrapper for brain tumor segmentation."""
    
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
    
    def __new__(cls, model_path: str = None):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(BrainTumorSegmenter, cls).__new__(cls)
            cls._instance.model_path = model_path
            cls._instance.model = None
            cls._instance.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            if model_path and os.path.exists(model_path):
                cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Load PyTorch model."""
        try:
            logger.info(f"Loading PyTorch model from {self.model_path}")
            logger.info(f"Using device: {self.device}")
            
            # Initialize model (2 channels: FLAIR, T1CE - matching Kaggle notebook)
            self.model = UNet(in_channels=2, num_classes=4)
            
            # Load checkpoint
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Handle different save formats
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                    logger.info(f"Loaded from checkpoint (epoch {checkpoint.get('epoch', 'unknown')})")
                else:
                    self.model.load_state_dict(checkpoint)
            else:
                self.model = checkpoint  # Direct model save
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("✅ PyTorch model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            self.model = None
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None
    
    def predict(self, image: np.ndarray) -> np.ndarray:
        """
        Predict segmentation.
        
        Args:
            image: Input image (batch, C, H, W) or (C, H, W) - numpy array
                   Preprocessor outputs (VOLUME_SLICES, 2, 128, 128)
            
        Returns:
            Segmentation mask (batch, C, H, W) - one-hot encoded probabilities
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        # Ensure correct format
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)  # Add batch dim
        
        # Process in batches to avoid OOM
        batch_size = 16  # Process 16 slices at a time
        num_samples = image.shape[0]
        output_list = []
        
        for i in range(0, num_samples, batch_size):
            batch_np = image[i : i + batch_size]
            
            # Input is already (B, C, H, W) from preprocessor
            image_tensor = torch.FloatTensor(batch_np).to(self.device)
            
            # Normalize
            if image_tensor.max() > 0:
                image_tensor = image_tensor / image_tensor.max()
            
            # Predict
            with torch.no_grad():
                batch_output = self.model(image_tensor)
                # Apply softmax to get probabilities
                batch_output = F.softmax(batch_output, dim=1)
                
            # Output is (B, C, H, W) - keep as-is
            output_list.append(batch_output.cpu().numpy())
            
            # Clear memory
            del image_tensor, batch_output
            if self.device == 'cuda':
                torch.cuda.empty_cache()
        
        # Concatenate results
        output_np = np.concatenate(output_list, axis=0)
        
        return output_np[0] if output_np.shape[0] == 1 else output_np
    
    def predict_class_mask(self, image: np.ndarray) -> np.ndarray:
        """Get class mask (argmax)."""
        pred = self.predict(image)
        # Pred is (B, C, H, W), so we want argmax over channel dim (axis=1)
        return np.argmax(pred, axis=1)
    
    def get_tumor_regions(self, class_mask: np.ndarray) -> dict:
        """Get tumor statistics."""
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