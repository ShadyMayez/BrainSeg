@echo off
cd /d "C:\Users\SONY\OneDrive\Desktop\brats_segmentation\backend"
echo Starting Brain Tumor Segmentation Backend...
echo Backend will run on http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/api/docs
echo.
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
