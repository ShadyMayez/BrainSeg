"""
Prediction endpoints for 2-channel brain tumor segmentation.
Matching Kaggle notebook: uses only FLAIR and T1CE modalities.
"""
import os
import tempfile
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import numpy as np
import nibabel as nib

from preprocessing.nifti_loader import BraTSPreprocessor
from models.unet_pytorch import get_segmenter
from utils.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def save_upload_file(upload_file: UploadFile, dest_path: Path) -> None:
    """Save an uploaded file to disk."""
    with open(dest_path, "wb") as f:
        content = upload_file.read()
        f.write(content)


def process_prediction(
    flair_path: str,
    t1ce_path: str,
    classes: str = "all"
) -> Dict[str, Any]:
    """
    Process prediction on uploaded files (2-channel: FLAIR + T1CE).
    
    Args:
        flair_path: Path to FLAIR NIfTI file
        t1ce_path: Path to T1CE NIfTI file
        classes: Comma-separated list of classes to include
    
    Returns:
        Dictionary with prediction results
    """
    # Get model path
    model_path = settings.get_model_path()
    
    # Get segmenter instance
    segmenter = get_segmenter(str(model_path))
    
    if not segmenter.is_loaded():
        raise HTTPException(
            status_code=503,
            detail=f"Model not loaded. Please check server configuration. Model path: {model_path}"
        )
    
    try:
        # Load and preprocess images (2 channels: FLAIR + T1CE)
        logger.info("Preprocessing 2-channel input (FLAIR + T1CE)...")
        preprocessor = BraTSPreprocessor(
            target_size=settings.TARGET_SIZE,
            volume_slices=settings.VOLUME_SLICES,
            volume_start_at=settings.VOLUME_START_AT
        )
        
        result = preprocessor.preprocess_for_inference(
            flair_path, t1ce_path
        )
        input_data = result['model_input']
        original_shape = result['original_shape']
        
        logger.info(f"Input shape: {input_data.shape}")
        
        # Run prediction
        logger.info("Running prediction...")
        prediction = segmenter.predict(input_data)
        
        logger.info(f"Prediction shape: {prediction.shape}")
        
        # Generate segmentation mask
        class_mask = segmenter.predict_class_mask(input_data)
        
        # Get tumor statistics
        stats = segmenter.get_tumor_regions(class_mask)
        
        # Filter by requested classes
        if classes != "all":
            requested = [int(c.strip()) for c in classes.split(",")]
            stats = {
                k: v for k, v in stats.items()
                if any(settings.CLASS_LABELS[i] == k for i in requested)
            }
        
        # Generate output files
        output_dir = Path(settings.OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create NIfTI segmentation mask
        mask_filename = f"segmentation_{os.urandom(4).hex()}.nii.gz"
        mask_path = output_dir / mask_filename
        
        # Post-process prediction back to original space
        output_volume = preprocessor.postprocess_prediction(
            prediction, original_shape
        )
        
        # Save as NIfTI
        nii_img = nib.Nifti1Image(output_volume, affine=np.eye(4))
        nib.save(nii_img, mask_path)
        
        # Create overlay image (middle slice)
        middle_slice_idx = settings.VOLUME_SLICES // 2
        overlay_filename = f"overlay_{os.urandom(4).hex()}.png"
        overlay_path = output_dir / overlay_filename
        
        # Generate visualization
        try:
            from visualization.visualize import create_overlay_image
            create_overlay_image(
                input_data[middle_slice_idx],
                class_mask[middle_slice_idx],
                overlay_path
            )
        except Exception as viz_e:
            logger.warning(f"Could not create overlay: {viz_e}")
            overlay_filename = None
        
        return {
            "status": "success",
            "segmentation_mask": f"/outputs/{mask_filename}",
            "overlay_image": f"/outputs/{overlay_filename}" if overlay_filename else None,
            "tumor_stats": stats,
            "class_distribution": {
                label: stats.get(label, {"pixel_count": 0, "percentage": 0})
                for label in settings.CLASS_LABELS.values()
            },
            "slice_thickness": None,
            "processed_slices": settings.VOLUME_SLICES,
            "input_shape": list(original_shape),
            "model_used": str(model_path.name)
        }
        
    except Exception as e:
        logger.exception("Prediction processing failed")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/")
async def predict(
    background_tasks: BackgroundTasks,
    flair: UploadFile = File(..., description="FLAIR modality NIfTI file"),
    t1ce: UploadFile = File(..., description="T1CE modality NIfTI file"),
    classes: str = Form("all", description="Comma-separated list of classes to include (default: all)")
):
    """
    Run tumor segmentation prediction on uploaded MRI files.
    
    Requires 2 modalities (matching Kaggle notebook):
    - **flair**: FLAIR modality NIfTI file
    - **t1ce**: T1CE (contrast-enhanced) modality NIfTI file
    - **classes**: Comma-separated list of classes to include (0=Non-tumor, 1=Necrotic/Core, 2=Edema, 3=Enhancing)
    """
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        logger.info("Received prediction request with 2 modalities (FLAIR + T1CE)")
        
        # Save uploaded files
        flair_path = temp_dir / flair.filename
        t1ce_path = temp_dir / t1ce.filename
        
        files_to_save = [
            (flair, flair_path, "FLAIR"),
            (t1ce, t1ce_path, "T1CE")
        ]
        
        for upload_file, save_path, mod_name in files_to_save:
            logger.info(f"Saving {mod_name} file: {upload_file.filename}")
            with open(save_path, "wb") as f:
                content = await upload_file.read()
                f.write(content)
            logger.info(f"Saved {mod_name} ({len(content)} bytes)")
        
        # Process prediction
        logger.info("Processing prediction...")
        result = process_prediction(
            str(flair_path),
            str(t1ce_path),
            classes
        )
        
        # Schedule cleanup
        background_tasks.add_task(shutil.rmtree, temp_dir, ignore_errors=True)
        
        logger.info("Prediction completed successfully")
        return result
        
    except HTTPException:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.exception("Prediction failed")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/classes")
async def get_classes():
    """Get available tumor classes."""
    return {
        i: label
        for i, label in settings.CLASS_LABELS.items()
    }


@router.get("/modalities")
async def get_modalities():
    """Get required modality names (2 channels - matching Kaggle notebook)."""
    return {
        "modalities": settings.MODALITIES,
        "count": len(settings.MODALITIES),
        "description": "2 BraTS modalities required: FLAIR and T1CE (matching Kaggle notebook)"
    }


@router.get("/model-info")
async def get_model_info():
    """Get information about the loaded model."""
    model_path = settings.get_model_path()
    segmenter = get_segmenter()
    
    return {
        "model_path": str(model_path),
        "model_exists": model_path.exists(),
        "model_loaded": segmenter.is_loaded(),
        "device": segmenter.device if segmenter.is_loaded() else None,
        "input_channels": settings.NUM_CHANNELS,
        "output_classes": settings.NUM_CLASSES,
        "target_size": settings.TARGET_SIZE,
        "volume_slices": settings.VOLUME_SLICES
    }
