"""
NIfTI Image Loader and Preprocessing Module
============================================
Handles loading and preprocessing of BraTS NIfTI format MRI scans.
Supports 4-channel input: FLAIR, T1, T1CE, T2.
Exact replication of notebook preprocessing logic.
"""
import numpy as np
import nibabel as nib
import cv2
from skimage.transform import resize
from typing import Tuple, List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BraTSPreprocessor:
    """
    Preprocessor for BraTS brain tumor MRI data.
    Implements the exact preprocessing pipeline from the notebook:
    1. Load 4 modalities (flair, t1, t1ce, t2)
    2. Normalize each modality to [0, 1]
    3. Stack into 4-channel volume
    4. Process slices (VOLUME_START_AT to VOLUME_START_AT + VOLUME_SLICES)
    5. Resize to (128, 128)
    """
    
    # All 4 modalities as used in the notebook
    MODALITIES = ['flair', 't1', 't1ce', 't2']
    
    # Class labels (same as notebook)
    CLASS_LABELS = {
        0: 'Non-tumor',
        1: 'Necrotic/Core',
        2: 'Edema',
        3: 'Enhancing Tumor'
    }
    
    # Class colors for visualization
    CLASS_COLORS = [
        'black',   # Class 0: Non-tumor
        'blue',    # Class 1: Necrotic/Core
        'pink',    # Class 2: Edema
        'cyan'     # Class 3: Enhancing Tumor
    ]
    
    # These values match the notebook exactly
    VOLUME_SLICES = 100
    VOLUME_START_AT = 22  # first slice of volume that we will include
    IMG_SIZE = 128
    
    def __init__(
        self,
        target_size: Tuple[int, int] = (128, 128),
        volume_slices: int = 100,
        volume_start_at: int = 22,
        num_classes: int = 4
    ):
        """
        Initialize preprocessor.
        
        Args:
            target_size: Target (H, W) for resizing
            volume_slices: Number of slices to process
            volume_start_at: Starting slice index
            num_classes: Number of output classes
        """
        self.target_size = target_size
        self.volume_slices = volume_slices
        self.volume_start_at = volume_start_at
        self.num_classes = num_classes
        
        logger.info(f"Preprocessor initialized:")
        logger.info(f"  Target size: {target_size}")
        logger.info(f"  Volume slices: {volume_slices}")
        logger.info(f"  Volume start: {volume_start_at}")
        logger.info(f"  Num classes: {num_classes}")
    
    def load_nifti(self, filepath: str) -> np.ndarray:
        """
        Load a NIfTI file.
        
        Args:
            filepath: Path to NIfTI file
        
        Returns:
            Numpy array of image data
        """
        try:
            nii_img = nib.load(filepath)
            return nii_img.get_fdata()
        except Exception as e:
            logger.error(f"Failed to load NIfTI file {filepath}: {e}")
            raise
    
    def normalize_modality(self, data: np.ndarray) -> np.ndarray:
        """
        Normalize modality data to [0, 1] range.
        Uses per-volume normalization as in the notebook.
        
        Args:
            data: Raw modality data
        
        Returns:
            Normalized data
        """
        data_min = np.min(data)
        data_max = np.max(data)
        
        if data_max > data_min:
            return (data - data_min) / (data_max - data_min)
        else:
            return data.astype(np.float32)
    
    def resize_slice(self, slice_data: np.ndarray) -> np.ndarray:
        """
        Resize a 2D slice to target size.
        
        Args:
            slice_data: 2D slice array
        
        Returns:
            Resized slice
        """
        return cv2.resize(slice_data, self.target_size, interpolation=cv2.INTER_AREA)
    
    def preprocess_for_inference(
        self,
        flair_path: str,
        t1_path: str,
        t1ce_path: str,
        t2_path: str
    ) -> Dict:
        """
        Preprocess 4 modalities for model inference.
        
        Args:
            flair_path: Path to FLAIR NIfTI file
            t1_path: Path to T1 NIfTI file
            t1ce_path: Path to T1CE NIfTI file
            t2_path: Path to T2 NIfTI file
        
        Returns:
            Dictionary containing:
                - 'model_input': Preprocessed data for model (VOLUME_SLICES, 4, H, W)
                - 'original_shape': Original volume shape
                - 'modalities': List of modality names
        """
        logger.info("Starting preprocessing for inference...")
        
        # Load all 4 modalities
        logger.info("Loading modalities...")
        flair = self.load_nifti(flair_path)
        t1 = self.load_nifti(t1_path)
        t1ce = self.load_nifti(t1ce_path)
        t2 = self.load_nifti(t2_path)
        
        original_shape = flair.shape
        logger.info(f"Original shape: {original_shape}")
        
        # Verify all modalities have same shape
        for name, data in [('flair', flair), ('t1', t1), ('t1ce', t1ce), ('t2', t2)]:
            if data.shape != original_shape:
                raise ValueError(
                    f"Shape mismatch: {name} has shape {data.shape}, "
                    f"expected {original_shape}"
                )
        
        # Normalize each modality
        logger.info("Normalizing modalities...")
        flair = self.normalize_modality(flair)
        t1 = self.normalize_modality(t1)
        t1ce = self.normalize_modality(t1ce)
        t2 = self.normalize_modality(t2)
        
        # Initialize output array: (VOLUME_SLICES, 4, H, W)
        # This matches the notebook's expected input format
        model_input = np.zeros(
            (self.volume_slices, 4, self.target_size[0], self.target_size[1]),
            dtype=np.float32
        )
        
        # Process each slice
        logger.info(f"Processing {self.volume_slices} slices...")
        for j in range(self.volume_slices):
            slice_pos = j + self.volume_start_at
            
            # Extract and resize each modality slice
            # Channel 0: FLAIR
            model_input[j, 0, :, :] = self.resize_slice(flair[:, :, slice_pos])
            # Channel 1: T1
            model_input[j, 1, :, :] = self.resize_slice(t1[:, :, slice_pos])
            # Channel 2: T1CE
            model_input[j, 2, :, :] = self.resize_slice(t1ce[:, :, slice_pos])
            # Channel 3: T2
            model_input[j, 3, :, :] = self.resize_slice(t2[:, :, slice_pos])
        
        logger.info(f"Preprocessing complete. Output shape: {model_input.shape}")
        
        return {
            'model_input': model_input,
            'original_shape': original_shape,
            'modalities': self.MODALITIES
        }
    
    def preprocess_with_segmentation(
        self,
        flair_path: str,
        t1_path: str,
        t1ce_path: str,
        t2_path: str,
        seg_path: str
    ) -> Dict:
        """
        Preprocess 4 modalities with ground truth segmentation.
        Used for training/validation, not inference.
        
        Args:
            flair_path: Path to FLAIR NIfTI file
            t1_path: Path to T1 NIfTI file
            t1ce_path: Path to T1CE NIfTI file
            t2_path: Path to T2 NIfTI file
            seg_path: Path to segmentation NIfTI file
        
        Returns:
            Dictionary containing preprocessed data and ground truth
        """
        # Get model input
        result = self.preprocess_for_inference(flair_path, t1_path, t1ce_path, t2_path)
        
        # Load segmentation
        seg = self.load_nifti(seg_path)
        
        # Convert class 4 to class 3 (as in notebook)
        seg[seg == 4] = 3
        
        # Initialize one-hot encoded segmentation
        # Shape: (VOLUME_SLICES, num_classes, H, W)
        seg_one_hot = np.zeros(
            (self.volume_slices, self.num_classes, self.target_size[0], self.target_size[1]),
            dtype=np.float32
        )
        
        # Process each slice
        for j in range(self.volume_slices):
            slice_pos = j + self.volume_start_at
            seg_slice = seg[:, :, slice_pos].astype(int)
            
            # Create one-hot encoding
            for c in range(self.num_classes):
                seg_one_hot[j, c, :, :] = self.resize_slice(
                    (seg_slice == c).astype(np.float32)
                )
        
        result['ground_truth'] = seg_one_hot
        
        return result
    
    def postprocess_prediction(
        self,
        prediction: np.ndarray,
        original_shape: Tuple[int, ...],
        target_orientation: str = 'axial'
    ) -> np.ndarray:
        """
        Post-process model prediction back to original space.
        
        Args:
            prediction: Model output (VOLUME_SLICES, 4, H, W)
            original_shape: Original volume shape (H, W, D)
            target_orientation: Target orientation
        
        Returns:
            Resized prediction in original space
        """
        # Get class predictions
        class_mask = np.argmax(prediction, axis=1)  # (VOLUME_SLICES, H, W)
        
        # Resize back to original dimensions
        output_volume = np.zeros(original_shape, dtype=np.uint8)
        
        for j in range(min(self.volume_slices, original_shape[2] - self.volume_start_at)):
            slice_pos = j + self.volume_start_at
            if slice_pos < original_shape[2]:
                # Resize slice back to original size
                resized_slice = cv2.resize(
                    class_mask[j].astype(np.float32),
                    (original_shape[0], original_shape[1]),
                    interpolation=cv2.INTER_NEAREST
                )
                output_volume[:, :, slice_pos] = resized_slice.astype(np.uint8)
        
        return output_volume


def load_and_preprocess_4channel(
    flair_path: str,
    t1_path: str,
    t1ce_path: str,
    t2_path: str,
    target_size: Tuple[int, int] = (128, 128)
) -> np.ndarray:
    """
    Convenience function to load and preprocess 4-channel BraTS data.
    
    Args:
        flair_path: Path to FLAIR NIfTI file
        t1_path: Path to T1 NIfTI file
        t1ce_path: Path to T1CE NIfTI file
        t2_path: Path to T2 NIfTI file
        target_size: Target size for resizing
    
    Returns:
        Preprocessed array ready for model input
    """
    preprocessor = BraTSPreprocessor(target_size=target_size)
    result = preprocessor.preprocess_for_inference(
        flair_path, t1_path, t1ce_path, t2_path
    )
    return result['model_input']
