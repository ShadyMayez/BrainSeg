"""
Visualization utilities for brain tumor segmentation.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Class colors for visualization (RGBA)
CLASS_COLORS = {
    0: (0, 0, 0, 0),          # Non-tumor: transparent
    1: (0, 0, 1, 0.5),        # Necrotic/Core: blue
    2: (1, 0.75, 0.8, 0.5),   # Edema: pink
    3: (0, 1, 1, 0.5)         # Enhancing Tumor: cyan
}


def create_overlay_image(
    input_channels: np.ndarray,
    segmentation_mask: np.ndarray,
    output_path: Path,
    reference_channel: int = 0
) -> None:
    """
    Create an overlay image of segmentation on top of MRI.
    
    Args:
        input_channels: Input array of shape (4, H, W)
        segmentation_mask: Segmentation mask of shape (H, W)
        output_path: Path to save the overlay image
        reference_channel: Which channel to use as background (0=FLAIR, 1=T1, 2=T1CE, 3=T2)
    """
    try:
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        # Get reference image
        ref_image = input_channels[reference_channel]
        
        # Plot original image
        axes[0].imshow(ref_image, cmap='gray')
        axes[0].set_title('Original MRI (FLAIR)')
        axes[0].axis('off')
        
        # Plot overlay
        axes[1].imshow(ref_image, cmap='gray')
        
        # Create colored mask
        colored_mask = np.zeros((*segmentation_mask.shape, 4))
        for class_idx, color in CLASS_COLORS.items():
            mask = segmentation_mask == class_idx
            for c in range(4):
                colored_mask[:, :, c][mask] = color[c]
        
        axes[1].imshow(colored_mask)
        axes[1].set_title('Segmentation Overlay')
        axes[1].axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='blue', alpha=0.5, label='Necrotic/Core'),
            Patch(facecolor='pink', alpha=0.5, label='Edema'),
            Patch(facecolor='cyan', alpha=0.5, label='Enhancing Tumor')
        ]
        axes[1].legend(handles=legend_elements, loc='lower left')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"Overlay image saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Failed to create overlay: {e}")
        raise


def create_segmentation_comparison(
    original: np.ndarray,
    ground_truth: Optional[np.ndarray],
    prediction: np.ndarray,
    output_path: Path,
    slice_idx: int = 0
) -> None:
    """
    Create a comparison image of original, ground truth, and prediction.
    
    Args:
        original: Original MRI image
        ground_truth: Ground truth segmentation (optional)
        prediction: Predicted segmentation
        output_path: Path to save comparison
        slice_idx: Slice index to visualize
    """
    try:
        if ground_truth is not None:
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            
            axes[0].imshow(original, cmap='gray')
            axes[0].set_title('Original MRI')
            axes[0].axis('off')
            
            axes[1].imshow(ground_truth)
            axes[1].set_title('Ground Truth')
            axes[1].axis('off')
            
            axes[2].imshow(prediction)
            axes[2].set_title('Prediction')
            axes[2].axis('off')
        else:
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            
            axes[0].imshow(original, cmap='gray')
            axes[0].set_title('Original MRI')
            axes[0].axis('off')
            
            axes[1].imshow(prediction)
            axes[1].set_title('Prediction')
            axes[1].axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        logger.info(f"Comparison image saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Failed to create comparison: {e}")
        raise
