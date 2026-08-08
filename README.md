# BrainSeg — Brain Tumor Segmentation from MRI

End-to-end medical-imaging application for segmenting brain-tumor sub-regions from multimodal MRI scans using a **U-Net deep learning model**, with a **FastAPI backend**, **React frontend**, and **Dockerized deployment**.

## Overview

BrainSeg uses the BraTS 2020 dataset to identify and segment clinically relevant tumor regions from MRI data. The project covers the full workflow from NIfTI preprocessing and model training through API serving and an interactive web interface.

The implementation focuses on three tumor-related regions:

- necrotic / non-enhancing tumor core
- peritumoral edema
- enhancing tumor

## System Architecture

```text
BraTS MRI volumes
      ↓
NIfTI preprocessing
      ↓
FLAIR + T1CE slice extraction
      ↓
Normalization / resizing
      ↓
2D U-Net segmentation
      ↓
FastAPI inference service
      ↓
React visualization interface
```

## Model

The project implements a **2D U-Net** designed for biomedical image segmentation.

| Component | Configuration |
| --- | --- |
| Input modalities | FLAIR + T1CE |
| Input shape | 2 × 128 × 128 |
| Output | 4-class segmentation map |
| Architecture | Encoder-decoder U-Net with skip connections |
| Parameters | ~7.7M trainable parameters |

Using FLAIR and T1CE instead of all four BraTS modalities reduces the input footprint while retaining modalities that are particularly informative for edema and enhancing/core tumor regions.

## Data Pipeline

1. Load NIfTI MRI volumes.
2. Select FLAIR and T1CE modalities.
3. Extract central 2D slices from each 3D scan.
4. Resize slices from 240×240 to 128×128.
5. Normalize intensities to the `[0, 1]` range.
6. Remap and one-hot encode segmentation labels.
7. Train the U-Net model and evaluate predicted masks.

## Evaluation

| Metric | Result |
| --- | ---: |
| Pixel Accuracy | 99.36% |
| Sensitivity | 99.15% |
| Specificity | 99.78% |
| Precision | 99.36% |
| Dice Score | 0.6480 |

> Pixel accuracy is strongly affected by the large background class, so the Dice score is the more informative overlap metric for evaluating tumor segmentation quality.

## Application Stack

| Layer | Technology |
| --- | --- |
| Deep learning | PyTorch |
| Model architecture | U-Net |
| Medical image processing | NIfTI-based preprocessing |
| API | FastAPI |
| Frontend | React + Vite |
| Deployment | Docker / Docker Compose |

## Project Structure

```text
BrainSeg/
├── backend/
│   ├── src/
│   │   ├── models/         # U-Net implementation
│   │   ├── api/            # Inference API routes
│   │   └── preprocessing/  # MRI and tensor processing
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   └── components/
│   └── package.json
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── run.bat
```

## Screenshots

<img width="1896" height="872" alt="BrainSeg application interface" src="https://github.com/user-attachments/assets/2cf14eda-5ea2-4e13-a1b1-0ddafe1d491d" />

<img width="1894" height="870" alt="BrainSeg MRI visualization" src="https://github.com/user-attachments/assets/973f0356-d5f3-457c-8a8d-090f7346ddd4" />

<img width="1896" height="1080" alt="BrainSeg segmentation results" src="https://github.com/user-attachments/assets/b2238e57-1bc6-48ed-b62a-43305b549c70" />

## Run Locally

### Requirements

- Python 3.10+
- Node.js 18+
- Docker, optional

### Clone

```bash
git clone https://github.com/ShadyMayez/BrainSeg.git
cd BrainSeg
```

### Application

On Windows, the included helper script starts the application stack:

```powershell
./run.bat
```

Frontend: `http://localhost:5173`  
Backend API: `http://localhost:8000`

### Docker

```bash
docker compose -f docker/docker-compose.yml up --build
```

## Dataset

The project is based on the **BraTS 2020 Brain Tumor Segmentation Challenge** dataset, which contains aligned multimodal MRI volumes and expert tumor annotations.

Dataset reference: [BraTS 2020 on Kaggle](https://www.kaggle.com/datasets/awsaf49/brats20-dataset-training-validation)

## Reference

Ronneberger, Fischer & Brox — [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)

---

Built by [ShadyMayez](https://github.com/ShadyMayez).