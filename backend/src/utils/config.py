"""
Configuration settings for the backend.
"""
import os
from pathlib import Path
from typing import List

# Maximum upload size (100 MB for direct uploads, larger via ngrok)
MAX_UPLOAD_SIZE = 100 * 1024 * 1024


class Settings:
    """Application settings."""
    
    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    BACKEND_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR.parent / "data"
    MODELS_DIR = BASE_DIR / "models"
    STATIC_DIR = BASE_DIR / "static"
    
    # Upload and output directories
    UPLOAD_DIR = BASE_DIR / "uploads"
    OUTPUT_DIR = BASE_DIR / "outputs"
    
    # Model path - now expects PyTorch .pth file
    # Use relative path for portability (Docker/Linux support)
    MODEL_PATH = MODELS_DIR / "saved_models" / "final_model.pth"
    
    # Alternative model paths to try
    ALT_MODEL_PATHS = [
        MODELS_DIR / "saved_models" / "best_model.pth",
        MODELS_DIR / "saved_models" / "model.pth",
        MODELS_DIR / "saved_models" / "final_model.pth",
    ]
    
    DATA_PATH = DATA_DIR
    
    # API settings
    HOST = os.getenv("API_HOST", "0.0.0.0")
    PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # ngrok settings for large file handling
    NGROK_ENABLED = os.getenv("NGROK_ENABLED", "false").lower() == "true"
    NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", "")
    NGROK_DOMAIN = os.getenv("NGROK_DOMAIN", "")
    
    # CORS origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.ngrok-free.app",  # Allow ngrok domains
        "*",  # Allow all in development
    ]
    
    # File upload settings
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(100 * 1024 * 1024)))  # 100 MB default
    ALLOWED_EXTENSIONS = {".nii", ".nii.gz", ".gz"}
    
    # Preprocessing settings (match notebook exactly)
    TARGET_SIZE = (128, 128)
    VOLUME_SLICES = 100
    VOLUME_START_AT = 22
    NUM_CLASSES = 4
    NUM_CHANNELS = 2  # 2 channels: flair, t1ce (matching Kaggle notebook)
    
    # Class labels
    CLASS_LABELS = {
        0: "Non-tumor",
        1: "Necrotic/Core",
        2: "Edema",
        3: "Enhancing Tumor"
    }
    
    CLASS_COLORS = {
        0: "#000000",  # Black
        1: "#0000FF",  # Blue
        2: "#FFC0CB",  # Pink
        3: "#00FFFF"   # Cyan
    }
    
    # Modality names (2 channels - matching Kaggle notebook)
    MODALITIES = ["flair", "t1ce"]
    
    @classmethod
    def get_model_path(cls) -> Path:
        """Get the first available model path."""
        # Check primary path first
        if cls.MODEL_PATH.exists():
            return cls.MODEL_PATH
        
        # Check alternative paths
        for path in cls.ALT_MODEL_PATHS:
            if path.exists():
                return path
        
        # Return default if none exist
        return cls.MODEL_PATH


settings = Settings()
