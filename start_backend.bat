@echo off
cd /d "C:\Users\SONY\OneDrive\Desktop\brats_segmentation\backend"
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001
pause
