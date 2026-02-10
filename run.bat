@echo off
REM Brain Tumor Segmentation - Run Script (Windows)
REM =================================================

echo =====================================
echo   Brain Tumor Segmentation
echo =====================================
echo.

set BACKEND_ONLY=false
set FRONTEND_ONLY=false

REM Parse arguments
:parse
if "%~1"=="" goto :main
if "%~1"=="--backend" (
    set BACKEND_ONLY=true
    shift
    goto :parse
)
if "%~1"=="--frontend" (
    set FRONTEND_ONLY=true
    shift
    goto :parse
)
echo Unknown option: %~1
echo Usage: %0 [--backend^|--frontend]
exit /b 1

:main
if "%BACKEND_ONLY%"=="true" (
    call :run_backend
    goto :end
)

if "%FRONTEND_ONLY%"=="true" (
    call :run_frontend
    goto :end
)

call :run_backend
timeout /t 3 /nobreak >nul
call :run_frontend

echo =====================================
echo   Application Started!
echo =====================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo.
echo Press Ctrl+C to stop
goto :end

:run_backend
echo Starting Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

if not exist "venv\.installed" (
    echo Installing backend dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    type nul > venv\.installed
)

if not exist "..\models\saved_models" mkdir ..\models\saved_models
if not exist "..\models\checkpoints" mkdir ..\models\checkpoints
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs

if not exist "..\models\saved_models\final_model.pth" (
    echo Warning: Model not found at models\saved_models\final_model.pth
    echo Please place your trained PyTorch model in this location
)

echo Backend starting at http://localhost:8000
echo API Docs: http://localhost:8000/api/docs

call python src\main.py
cd ..
goto :eof

:run_frontend
echo Starting Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

echo Frontend starting at http://localhost:5173

call npm run dev
cd ..
goto :eof

:end
pause
