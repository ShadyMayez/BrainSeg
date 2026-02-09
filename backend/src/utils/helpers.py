"""
Helper utilities for the backend.
"""

import os
import hashlib
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path


def validate_nifti_file(filepath: str) -> bool:
    """Validate if file is a valid NIfTI file."""
    if not os.path.exists(filepath):
        return False
    
    valid_extensions = ['.nii', '.nii.gz', '.gz']
    return any(filepath.endswith(ext) for ext in valid_extensions)


def get_file_hash(filepath: str) -> str:
    """Compute MD5 hash of file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_image_statistics(image: np.ndarray) -> Dict:
    """Compute basic image statistics."""
    return {
        'shape': list(image.shape),
        'dtype': str(image.dtype),
        'min': float(np.min(image)),
        'max': float(np.max(image)),
        'mean': float(np.mean(image)),
        'std': float(np.std(image)),
        'non_zero_pixels': int(np.count_nonzero(image))
    }


def get_mask_statistics(mask: np.ndarray) -> Dict:
    """Compute mask statistics."""
    # Convert to class indices if one-hot
    if len(mask.shape) == 4 and mask.shape[-1] == 4:
        mask = np.argmax(mask, axis=-1)
    
    total_pixels = mask.size
    class_names = {
        0: 'Non-tumor',
        1: 'Necrotic/Core',
        2: 'Edema',
        3: 'Enhancing Tumor'
    }
    
    stats = {'total_pixels': total_pixels}
    for class_idx, class_name in class_names.items():
        count = int(np.sum(mask == class_idx))
        percentage = float((count / total_pixels) * 100)
        stats[class_name] = {
            'pixel_count': count,
            'percentage': round(percentage, 2)
        }
    
    return stats


def ensure_dir(directory: Path):
    """Create directory if it doesn't exist."""
    directory.mkdir(parents=True, exist_ok=True)


def cleanup_temp_files(directory: Path, max_age_hours: int = 24):
    """Clean up temporary files older than max_age_hours."""
    import time
    from datetime import datetime, timedelta
    
    if not directory.exists():
        return
    
    cutoff_time = time.time() - (max_age_hours * 3600)
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                except Exception:
                    pass
