# Brain Tumor Segmentation (BraTS 2020) 🧠

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18-cyan)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

A deep learning application for automated 3D brain tumor segmentation using the U-Net architecture. This project utilizes the BraTS 2020 dataset to identify and segment tumor sub-regions (edema, enhancing tumor, necrotic core) from multimodal MRI scans.

---

## 📑 Table of Contents
- [Introduction](#-introduction)
- [Dataset Details](#-dataset-details)
- [Data Preprocessing](#-data-preprocessing)
- [Model Architecture](#-model-architecture)
- [Performance](#-performance)
- [Deployment & Usage](#-deployment--usage)
  - [Local Setup](#local-setup)
  - [Docker Deployment](#docker-deployment)
- [Project Structure](#-project-structure)

---

## 📌 Introduction
Image segmentation plays a pivotal role in medical imaging by enabling precise delineation of anatomical structures and pathologies. In neuro-oncology, accurate segmentation of brain tumors from MRI scans is essential for diagnosis, treatment planning, and monitoring.

This project implements a **2D U-Net** to process multi-modal MRI data (FLAIR and T1CE) and generate voxel-wise segmentation maps for:
1.  **Necrotic/Core Tumor**
2.  **Peritumoral Edema**
3.  **Enhancing Tumor**

---

## 📂 Dataset Details
The model is trained on the **[BraTS 2020 (Brain Tumor Segmentation) Challenge Dataset](https://www.kaggle.com/datasets/awsaf49/brats20-dataset-training-validation)**. The dataset consists of 3D MRI scans from glioma patients.

### Modalities
Each patient case includes 4 aligned 3D volumes:
- **T1**: Native T1-weighted.
- **T1CE**: Post-contrast T1-weighted (Contrast Enhanced).
- **T2**: T2-weighted.
- **FLAIR**: T2 Fluid Attenuated Inversion Recovery.

> **Our Approach**: To optimize computational efficiency, we utilize only **T1CE** ( tumor core) and **FLAIR** (edema), reducing the input channels from 4 to 2.

### Segmentation Classes
The dataset includes expert annotations mapped to the following classes:
- **Label 0**: Background / Not Tumor
- **Label 1**: Necrotic and Non-Enhancing Tumor Core (NCR/NET)
- **Label 2**: Peritumoral Edema (ED)
- **Label 4**: GD-Enhancing Tumor (ET) -> *Remapped to Label 3 for continuity*

---

## 🛠️ Data Preprocessing
To prepare the 3D MRI volumes for the 2D U-Net, the following pipeline is applied:

1.  **Modality Selection**: Loading `_flair.nii` and `_t1ce.nii` files.
2.  **Slice Extraction**: Processing 3D volumes as a stack of 2D slices. We focus on the central slices (approx. 60-135) where the tumor is most prominent.
3.  **Resizing**: Images are resized from `240x240` to `128x128` to reduce memory usage.
4.  **Normalization**: Min-Max scaling is applied to normalize pixel intensities to the `[0, 1]` range.
5.  **One-Hot Encoding**: Segmentation masks are converted into 4-channel one-hot encoded tensors.

---

## 🏗️ Model Architecture
We utilize the **U-Net** architecture, a standard for biomedical image segmentation. It consists of a contracting path (encoder) to capture context and a symmetric expanding path (decoder) for precise localization.

### Key Features
- **Encoder**: 5 blocks of Convolution + ReLU + Max Pooling.
- **Decoder**: 4 blocks of Up-Sampling + Concatenation (Skip Connections) + Convolution.
- **Input**: `(Batch, 2, 128, 128)` [FLAIR, T1CE].
- **Output**: `(Batch, 4, 128, 128)` [Probability map for 4 classes].
- **Parameters**: ~7.7 Million trainable parameters.

---

## 📊 Performance
The model was evaluated on the test set using discrete segmentation metrics.

| Metric | Score | Description |
| :--- | :--- | :--- |
| **Accuracy** | **99.36%** | Overall pixel-wise classification accuracy. |
| **Sensitivity** | **99.15%** | True Positive Rate (Recall). |
| **Specificity** | **99.78%** | True Negative Rate. |
| **Precision** | **99.36%** | Positive Predictive Value. |
| **Dice Score** | **0.6480** | F1-Score equivalent for segmentation overlap. |

*Note: High accuracy is partially due to the class imbalance (large background area).*

---

## 🚀 Deployment & Usage

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (optional)

### Local Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/BrainSeg.git
    cd BrainSeg
    ```

2.  **Start the Application**:
    Run the helper script to set up backend (FastAPI) and frontend (React) automatically.
    ```powershell
    ./run.bat
    ```

3.  **Access the Dashboard**:
    - Frontend: `http://localhost:5173`
    - Backend API: `http://localhost:8000`

### 🐳 Docker Deployment
Run the entire stack in isolated containers.

1.  **Build and Run**:
    ```powershell
    docker-compose -f docker/docker-compose.yml up --build
    ```

2.  **Access App**:
    - Web UI: `http://localhost:5173`

---

## � Project Structure
```
BrainSeg/
├── backend/                # FastAPI Application
│   ├── src/
│   │   ├── models/         # U-Net PyTorch Implementation
│   │   ├── api/            # API Routes
│   │   └── preprocessing/  # NIfTI loading and tensor conversion
│   └── requirements.txt
│
├── frontend/               # React + Vite Application
│   ├── src/
│   │   ├── pages/          # UI Pages
│   │   └── components/     # Reusable Components
│   └── package.json
│
├── docker/                 # Docker Configuration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
└── run.bat                 # Windows Startup Script
```

---
<img width="1896" height="872" alt="Untitled" src="https://github.com/user-attachments/assets/2cf14eda-5ea2-4e13-a1b1-0ddafe1d491d" />
<img width="1894" height="870" alt="Untitled1" src="https://github.com/user-attachments/assets/973f0356-d5f3-457c-8a8d-090f7346ddd4" />
<img width="1896" height="1080" alt="Untitled2" src="https://github.com/user-attachments/assets/b2238e57-1bc6-48ed-b62a-43305b549c70" />




## 📚 References
- **U-Net**: [Ronneberger et al., 2015](https://arxiv.org/abs/1505.04597)
- **BraTS 2020 Data**: [Kaggle Dataset](https://www.kaggle.com/datasets/awsaf49/brats20-dataset-training-validation)
