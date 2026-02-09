# 🧠 Brain Tumor Segmentation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange.svg)](https://tensorflow.org/)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3+-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A production-ready web application for **3D Brain Tumor Segmentation** using deep learning. This project implements a **U-Net architecture with EfficientNetB0 backbone** trained on the BraTS 2020 dataset.

## 🏗️ Architecture

This project uses a modern **full-stack architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Prediction │  │   Analysis  │  │    About    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  React 18 + TypeScript + Vite + Tailwind CSS + Zustand      │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Prediction │  │    Data     │  │   Health    │         │
│  │   Routes    │  │   Routes    │  │   Routes    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  FastAPI + TensorFlow + NiBabel + scikit-image              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Model (U-Net)                            │
│                                                              │
│  Input: (128, 128, 3) → U-Net + EfficientNetB0 → (128,128,4)│
└─────────────────────────────────────────────────────────────┘
```

## 🌟 Features

- **🖥️ Modern React Frontend**: Built with Vite, TypeScript, and Tailwind CSS
- **⚡ FastAPI Backend**: High-performance Python API with async support
- **🧠 Deep Learning Model**: U-Net with EfficientNetB0 for accurate segmentation
- **📊 Interactive Visualizations**: Real-time MRI viewing with tumor overlay
- **📈 Data Analysis Dashboard**: Explore dataset statistics and training metrics
- **🏗️ MLOps Architecture**: Production-ready folder structure and best practices

## 📁 Project Structure

```
brats_segmentation/
├── backend/                    # FastAPI Backend
│   ├── src/
│   │   ├── api/               # API routes
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── prediction.py
│   │   │       └── data_analysis.py
│   │   ├── models/            # U-Net model
│   │   │   └── unet_model.py
│   │   ├── preprocessing/     # NIfTI loader
│   │   │   └── nifti_loader.py
│   │   ├── visualization/     # Plotting functions
│   │   │   └── visualize.py
│   │   ├── utils/             # Helper functions
│   │   │   ├── config.py
│   │   │   └── helpers.py
│   │   └── main.py            # FastAPI entry point
│   ├── requirements.txt
│   └── tests/
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   │   ├── Layout/        # Navbar, Sidebar
│   │   │   ├── UI/            # Button, Card, etc.
│   │   │   └── Prediction/    # FileUpload, ResultsPanel
│   │   ├── pages/             # Page components
│   │   │   ├── PredictionPage.tsx
│   │   │   ├── DataAnalysisPage.tsx
│   │   │   └── AboutPage.tsx
│   │   ├── services/          # API client
│   │   │   └── api.ts
│   │   ├── store/             # State management (Zustand)
│   │   │   └── useAppStore.ts
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   └── styles/            # Tailwind CSS
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── data/                       # Dataset storage
│   ├── raw/                   # Raw NIfTI files
│   └── processed/             # Preprocessed data
│
├── models/                     # Saved model weights
│   ├── saved_models/          # Best model
│   └── checkpoints/           # Training checkpoints
│
├── docker/                     # Docker configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm/yarn
- 8GB+ RAM recommended
- GPU optional (CUDA-compatible for faster inference)

### 1. Clone and Setup

```bash
git clone https://github.com/example/brats-segmentation.git
cd brats-segmentation
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python src/main.py
```

The backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/api/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Add Model (Optional)

Place your trained model at:
```
models/saved_models/best_model.keras
```

## 📖 Usage

### Web Application

1. Navigate to `http://localhost:5173`
2. Go to the **Prediction** page
3. Upload 3 NIfTI files:
   - FLAIR modality (`*_flair.nii`)
   - T1ce modality (`*_t1ce.nii`)
   - T2 modality (`*_t2.nii`)
4. Click **"Run Segmentation"**
5. View results with tumor overlay and statistics

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/` | GET | Health check |
| `/api/health/model` | GET | Model status |
| `/api/predict/` | POST | Run segmentation |
| `/api/predict/classes` | GET | Get class info |
| `/api/data/dataset-info` | GET | Dataset overview |
| `/api/data/training-metrics` | GET | Training metrics |
| `/api/data/model-architecture` | GET | Model architecture |

## 🔬 Preprocessing Pipeline

The preprocessing follows the exact pipeline from the BraTS 2020 notebook:

1. **Load NIfTI files** using nibabel
2. **Normalize** each modality: `(img - min) / (max - min)`
3. **Select 3 channels**: FLAIR, T1ce, T2 (excludes T1)
4. **Crop slices**: Remove 60 slices from start and end
5. **Resize** to 128×128 using bilinear interpolation
6. **One-hot encode** masks to 4 classes

### 4-Channel to 3-Channel Conversion

```python
# Original BraTS: 4 modalities
modalities = ['flair', 't1', 't1ce', 't2']

# Model input: 3 modalities (excludes t1)
selected_modalities = ['flair', 't1ce', 't2']

# Stack into 3-channel volume
image = np.stack([flair, t1ce, t2], axis=-1)  # Shape: (H, W, D, 3)
```

## 📊 Performance Metrics

| Metric | Training | Validation |
|--------|----------|------------|
| Accuracy | ~99% | ~98.8% |
| Dice Coefficient | ~0.99 | ~0.98 |
| Precision | ~0.97 | ~0.96 |
| Sensitivity | ~0.96 | ~0.95 |
| Specificity | ~0.99 | ~0.99 |

### Training Configuration

- **Epochs**: 30
- **Batch Size**: 16
- **Optimizer**: Adam
- **Loss**: Weighted Dice Loss
- **Class Weights**: [0.45, 0.25, 0.20, 0.20]

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build separately
docker-compose up --build backend
docker-compose up --build frontend
```

Access the application:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📚 Dataset

This project uses the **BraTS 2020** (Brain Tumor Segmentation) dataset:

- **Training Set**: 294 patients
- **Validation Set**: 74 patients
- **Total Slices**: 12,880
- **Modalities**: FLAIR, T1, T1ce, T2
- **Annotations**: Expert-annotated segmentation masks

Download from: [CBICA BraTS](https://www.med.upenn.edu/cbica/brats/)

## 📝 Citation

If you use this project in your research, please cite:

```bibtex
@article{brats2020,
  title={The Multimodal Brain Tumor Image Segmentation Benchmark (BRATS)},
  author={Menze, Bjoern H et al.},
  journal={IEEE Transactions on Medical Imaging},
  year={2015}
}

@inproceedings{unet2015,
  title={U-Net: Convolutional Networks for Biomedical Image Segmentation},
  author={Ronneberger, Olaf et al.},
  booktitle={MICCAI},
  year={2015}
}
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [BraTS Challenge](https://www.med.upenn.edu/cbica/brats/) for the dataset
- [TensorFlow](https://tensorflow.org/) for the deep learning framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

<p align="center">
  🧠 Built with ❤️ for advancing medical AI research
</p>
