# Brain Tumor Segmentation - Application Status & Setup Guide

## ✅ Current Status

Both backend and frontend are now **RUNNING AND WORKING**:

### Backend Service
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Port**: 8000
- **Status**: ✅ Running (No reload mode - stable)
- **Process**: Python Uvicorn
- **Startup**: `start_backend_stable.bat`

### Frontend Application
- **URL**: http://localhost:5174
- **Port**: 5174 (5173 was in use)
- **Status**: ✅ Running
- **Build Tool**: Vite
- **Framework**: React + TypeScript
- **Startup**: `start_frontend.bat`

---

## 🚀 How to Start the Application

### Option 1: Using Batch Scripts (Recommended for Windows)

Open two command prompts (or PowerShell windows) in the project root directory:

**Terminal 1 - Start Backend:**
```bash
./start_backend_stable.bat
```

**Terminal 2 - Start Frontend:**
```bash
./start_frontend.bat
```

Then open your browser to: **http://localhost:5174**

### Option 2: Manual Startup

**Start Backend:**
```bash
cd backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

**Start Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

---

## 📋 Recent Fixes Applied

1. **Fixed Reload Issues**: Disabled `--reload` flag in backend startup to prevent crashes
2. **Added Port 5174**: Added localhost:5174 to CORS allowed origins
3. **Stable Server**: Backend now runs reliably without auto-reload watchfiles
4. **CORS Configuration**: Properly configured to accept requests from frontend

---

## ⚙️ Configuration Details

### Backend Configuration (`backend/src/utils/config.py`)
- **Model Path**: `models/saved_models/best_model.keras`
- **API Host**: 127.0.0.1
- **API Port**: 8000
- **Upload Directory**: `backend/uploads/`
- **Output Directory**: `backend/outputs/`
- **Max File Size**: 100 MB
- **Allowed Extensions**: `.nii`, `.nii.gz`, `.gz`

### CORS Settings (Allowed Origins)
- http://localhost:3000
- http://localhost:5173
- http://localhost:5174
- http://127.0.0.1:3000
- http://127.0.0.1:5173
- http://127.0.0.1:5174
- `*` (Allow all for development)

---

## 📂 Important Files

### Backend
- **Entry Point**: `backend/src/main.py`
- **Health Routes**: `backend/src/api/routes/health.py`
- **Prediction Routes**: `backend/src/api/routes/prediction.py`
- **Model Wrapper**: `backend/src/models/unet_model.py`
- **Preprocessing**: `backend/src/preprocessing/nifti_loader.py`
- **Visualization**: `backend/src/visualization/visualize.py`

### Frontend  
- **Main App**: `frontend/src/App.tsx`
- **API Service**: `frontend/src/services/api.ts`
- **Pages**: `frontend/src/pages/`
- **Components**: `frontend/src/components/`

### Model
- **Location**: `models/saved_models/best_model.keras`
- **Status**: Directory ready (awaiting model file)

---

## 🔧 Next Steps

1. **Place Model File**: Copy `best_model.keras` to `models/saved_models/`
   - If you already have this file, place it at the correct path
   - Backend will load it when you first try to predict

2. **Test File Upload**:
   - Navigate to http://localhost:5174
   - Click on the "Prediction" tab
   - Upload three NIfTI files:
     - FLAIR MRI image (.nii or .nii.gz)
     - T1ce MRI image (.nii or .nii.gz)  
     - T2 MRI image (.nii or .nii.gz)
   - The backend will process and return segmentation results

3. **View API Documentation**:
   - Open http://localhost:8000/api/docs
   - Try endpoints directly from the Swagger UI

---

## 🐛 Troubleshooting

### Backend Won't Start
1. Check if port 8000 is in use: `netstat -ano | findstr :8000`
2. Kill the process: `taskkill /PID <PID> /F`
3. Restart with: `./start_backend_stable.bat`

### Frontend Shows CORS Errors
- Backend must be running on port 8000
- Verify: `curl http://localhost:8000/api/health/`
- Check that CORS middleware is in `backend/src/main.py`

### File Upload Fails
1. Verify backend is running: Check terminal output for "Application startup complete"
2. Check file format: Must be NIfTI files (.nii or .nii.gz)
3. Check file size: Max 100 MB per file
4. View backend logs for detailed error messages

### Port Already in Use
- Backend default: 8000
- Frontend default: 5173 (falls back to 5174 if in use)
- If you need different ports, update the batch files or use `--port` flag

---

## 📊 API Endpoints

### Health Endpoints
- `GET /api/health/` - Check API health
- `GET /api/health/model` - Check model status and loaded classes
- `GET /api/health/config` - Get application configuration

### Prediction Endpoints  
- `POST /api/predict/` - Upload MRI files and get segmentation
- `GET /api/predict/classes` - Get information about segmentation classes

### Data Analysis Endpoints
- `GET /api/data/dataset-info` - Dataset statistics
- `GET /api/data/training-metrics` - Model training metrics
- `GET /api/data/model-architecture` - Model architecture details

---

## 🎯 Success Indicators

When everything is working correctly:
1. ✅ Backend terminal shows "Application startup complete"
2. ✅ Frontend terminal shows "ready in X ms" and listening on port
3. ✅ Browser loads http://localhost:5174 without errors
4. ✅ No CORS errors in browser console
5. ✅ File upload page displays without errors
6. ✅ Can submit files for prediction

---

## 💡 Development Notes

- **No Hot Reload for Backend**: Disable reload mode on Windows due to watchfiles issues
- **Frontend Hot Reload**: Enabled and working in Vite
- **Python Version**: 3.14.2
- **Node Version**: Check with `node --version`
- **All Dependencies**: Already installed in virtual environment

---

## 📝 Version Information

- **FastAPI**: 0.128.0
- **TensorFlow**: 2.20.0
- **Keras**: 3.12.1
- **React**: 18.2.0
- **Vite**: 5.4.21
- **TypeScript**: 5.2.2
- **Tailwind CSS**: 3.3.5

---

## 🎓 For Bug Reports

If something isn't working:
1. Check both terminals for error messages
2. Look at browser console (F12) for CORS/network errors
3. Check backend health endpoint: http://localhost:8000/api/health/
4. Review full stack trace in terminal
5. Verify model file exists at `models/saved_models/best_model.keras`

---

Generated: Application Successfully Started
Status: Both services running and ready for testing
