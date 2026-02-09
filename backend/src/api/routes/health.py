"""
Health check endpoints.
"""
import os
import sys
from pathlib import Path
from fastapi import APIRouter
import torch
import numpy as np
import nibabel as nib

from utils.config import settings
from models.unet_pytorch import get_segmenter

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "brain-tumor-segmentation-api",
        "version": "2.0.0",
        "framework": "pytorch"
    }


@router.get("/model")
async def model_health():
    """Check model status."""
    model_path = settings.get_model_path()
    segmenter = get_segmenter()
    
    return {
        "model_path": str(model_path),
        "model_exists": model_path.exists(),
        "model_loaded": segmenter.is_loaded(),
        "device": segmenter.device if segmenter.is_loaded() else None,
        "input_channels": settings.NUM_CHANNELS,
        "output_classes": settings.NUM_CLASSES
    }


@router.get("/config")
async def get_config():
    """Get application configuration."""
    return {
        "preprocessing": {
            "target_size": settings.TARGET_SIZE,
            "volume_slices": settings.VOLUME_SLICES,
            "volume_start_at": settings.VOLUME_START_AT,
            "num_classes": settings.NUM_CLASSES,
            "num_channels": settings.NUM_CHANNELS
        },
        "modalities": settings.MODALITIES,
        "class_labels": settings.CLASS_LABELS,
        "class_colors": settings.CLASS_COLORS,
        "max_file_size": settings.MAX_FILE_SIZE,
        "ngrok_enabled": settings.NGROK_ENABLED
    }


@router.get("/environment")
async def environment_check():
    """Check environment and dependencies."""
    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    cuda_version = torch.version.cuda if cuda_available else None
    
    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Get PyTorch version
    pytorch_version = torch.__version__
    
    # Get NumPy version
    numpy_version = np.__version__
    
    # Get Nibabel version
    nibabel_version = nib.__version__
    
    return {
        "python_version": python_version,
        "pytorch_version": pytorch_version,
        "numpy_version": numpy_version,
        "nibabel_version": nibabel_version,
        "cuda_available": cuda_available,
        "cuda_version": cuda_version,
        "device_count": torch.cuda.device_count() if cuda_available else 0,
        "device_name": torch.cuda.get_device_name(0) if cuda_available else None
    }
