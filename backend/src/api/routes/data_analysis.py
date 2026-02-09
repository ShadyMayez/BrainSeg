"""
Data analysis endpoints.
"""
from fastapi import APIRouter
from utils.config import settings

router = APIRouter()


@router.get("/dataset-info")
async def get_dataset_info():
    """Get dataset information."""
    return {
        "dataset": "BraTS 2020",
        "description": "Brain Tumor Segmentation dataset with 4 MRI modalities",
        "modalities": settings.MODALITIES,
        "num_modalities": len(settings.MODALITIES),
        "classes": settings.CLASS_LABELS,
        "num_classes": settings.NUM_CLASSES,
        "preprocessing": {
            "target_size": settings.TARGET_SIZE,
            "volume_slices": settings.VOLUME_SLICES,
            "volume_start_at": settings.VOLUME_START_AT
        }
    }


@router.get("/feature-statistics")
async def get_feature_statistics():
    """Get feature statistics."""
    return {
        "modalities": {
            mod: {
                "description": get_modality_description(mod),
                "normalization": "per-volume min-max to [0, 1]"
            }
            for mod in settings.MODALITIES
        }
    }


@router.get("/training-metrics")
async def get_training_metrics():
    """Get training metrics (placeholder)."""
    return {
        "note": "Training metrics not available in inference mode",
        "model_type": "PyTorch U-Net",
        "input_channels": settings.NUM_CHANNELS,
        "output_classes": settings.NUM_CLASSES
    }


def get_modality_description(modality: str) -> str:
    """Get description for a modality."""
    descriptions = {
        "flair": "T2-FLAIR (Fluid Attenuated Inversion Recovery) - suppresses fluid signals",
        "t1": "Native T1-weighted - reveals tissue structure and composition",
        "t1ce": "T1-weighted with Gadolinium contrast enhancement - highlights abnormalities",
        "t2": "T2-weighted - highlights fluid content within tissues"
    }
    return descriptions.get(modality, "Unknown modality")
