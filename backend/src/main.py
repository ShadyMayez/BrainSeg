"""
FastAPI Backend for Brain Tumor Segmentation
============================================
Main application entry point.
PyTorch-based with 4-channel input support.
"""
import os
import sys
from contextlib import asynccontextmanager

# Add src to path early
sys.path.insert(0, os.path.dirname(__file__))

# Import FastAPI and dependencies
try:
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import JSONResponse
    from starlette.middleware.base import BaseHTTPMiddleware
except ImportError as e:
    print(f"ERROR: Failed to import FastAPI: {e}")
    sys.exit(1)

# Import routes and config
try:
    from api.routes import prediction, data_analysis, health
    from utils.config import settings
    from models.unet_pytorch import get_segmenter
except ImportError as e:
    print(f"ERROR: Failed to import routes: {e}")
    sys.exit(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    print("=" * 60)
    print("🧠 Brain Tumor Segmentation API Starting...")
    print(f"📦 Version: 2.0.0 (PyTorch - 2 Channel)")
    print(f"📁 Model path: {settings.get_model_path()}")
    print(f"📊 Data path: {settings.DATA_PATH}")
    print(f"🔢 Input channels: {settings.NUM_CHANNELS}")
    print(f"🎯 Output classes: {settings.NUM_CLASSES}")
    print("=" * 60)
    
    # Create directories
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    os.makedirs(settings.STATIC_DIR, exist_ok=True)
    
    # Try to load model on startup
    model_path = settings.get_model_path()
    if model_path.exists():
        print(f"📥 Loading model from {model_path}...")
        segmenter = get_segmenter(str(model_path))
        if segmenter.is_loaded():
            print(f"✅ Model loaded successfully on {segmenter.device}")
        else:
            print(f"⚠️  Failed to load model from {model_path}")
            print(f"   Predictions will fail until a valid model is provided.")
    else:
        print(f"⚠️  Model file not found: {model_path}")
        print(f"   Please place your model at: {settings.MODEL_PATH}")
        print(f"   Predictions will fail until a model is provided.")
    
    yield
    
    print("=" * 60)
    print("🛑 Brain Tumor Segmentation API Shutting down...")
    print("=" * 60)


# Create FastAPI app
app = FastAPI(
    title="Brain Tumor Segmentation API",
    description="2-Channel MRI Analysis (FLAIR + T1CE) using PyTorch Deep Learning",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


# 404 handler with CORS
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    response = JSONResponse(
        status_code=404,
        content={"detail": "Not found", "path": str(request.url.path)}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc):
    import traceback
    print(f"\n[GLOBAL_EXCEPTION] {type(exc).__name__}: {str(exc)}")
    traceback.print_exc()
    
    response = JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.middleware("http")
async def limit_upload_size(request, call_next):
    """Limit upload size."""
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.MAX_FILE_SIZE:
            response = JSONResponse(
                status_code=413,
                content={"detail": f"File too large. Maximum size is {settings.MAX_FILE_SIZE / (1024*1024):.0f}MB"}
            )
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response
    return await call_next(request)


# Include routers
print("[APP] Registering routes...")
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(prediction.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(data_analysis.router, prefix="/api/data", tags=["Data Analysis"])

# Static files
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Brain Tumor Segmentation API",
        "version": "2.0.0",
        "framework": "PyTorch",
        "input_channels": settings.NUM_CHANNELS,
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "predict": "/api/predict",
            "data": "/api/data"
        }
    }


@app.get("/api")
async def api_info():
    """API information."""
    return {
        "name": "Brain Tumor Segmentation API",
        "version": "2.0.0",
        "framework": "PyTorch",
        "input_channels": settings.NUM_CHANNELS,
        "modalities": settings.MODALITIES,
        "classes": settings.CLASS_LABELS
    }


# Print registered routes
print("\n[APP] Registered routes:")
for route in app.routes:
    if hasattr(route, 'methods'):
        print(f"  {list(route.methods)} {route.path}")
print()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info"
    )
