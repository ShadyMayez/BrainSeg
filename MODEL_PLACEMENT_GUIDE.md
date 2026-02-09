# 📍 Model File Placement Guide

## Where to Place Your Model

Your model file `best_model.keras` should be placed in:

```
📦 brats_segmentation (Project Root)
│
├── 📂 models/
│   └── 📂 saved_models/
│       └── 📄 best_model.keras  ⬅️ PUT YOUR MODEL FILE HERE
│
├── backend/
├── frontend/
├── docker/
├── assets/
└── ... (other files)
```

## Exact Path

```
c:\Users\SONY\OneDrive\Desktop\brats_segmentation\models\saved_models\best_model.keras
```

## How the Backend Finds It

The configuration file automatically looks for the model at this location:

**File:** `backend/src/utils/config.py`

```python
# Project paths
BASE_DIR = Path(__file__).parent.parent.parent  # = backend/
MODELS_DIR = BASE_DIR.parent / "models"         # = project_root/models/

# Model path
MODEL_PATH = MODELS_DIR / "saved_models" / "best_model.keras"
```

This resolves to: `project_root/models/saved_models/best_model.keras`

## Verification Checklist

- [ ] Directory `models/` exists in project root
- [ ] Directory `models/saved_models/` exists
- [ ] File `best_model.keras` is in `models/saved_models/`
- [ ] File is readable (not corrupted)
- [ ] File permissions allow read access

## Quick Verification Command

After placing the file, verify it exists:

```bash
# Windows
dir "c:\Users\SONY\OneDrive\Desktop\brats_segmentation\models\saved_models\"

# Should show:
# - best_model.keras

# Linux/Mac
ls -la ~/Desktop/brats_segmentation/models/saved_models/

# Should show:
# - best_model.keras (with file size)
```

## What Happens When App Starts

1. Backend initializes (`backend/src/main.py`)
2. Checks for model at: `models/saved_models/best_model.keras`
3. Loads model into TensorFlow/Keras
4. Makes it available for predictions
5. If missing, API will show error message

## Error Message If Model Not Found

If you don't place the model file, you'll see:
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/saved_models/best_model.keras'
```

**Solution:** Place the model file at the path shown above.

---

## 📂 Directory Structure (After Placement)

```
brats_segmentation/
├── models/
│   └── saved_models/
│       └── best_model.keras          ✅ [PLACE HERE]
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   └── unet_model.py          (Model architecture definition)
│   │   ├── preprocessing/
│   │   ├── visualization/
│   │   ├── api/routes/
│   │   └── utils/
│   │       └── config.py              (Points to models/saved_models/...)
│   └── requirements.txt
├── frontend/
├── docker/
└── ...
```

## 🔑 Key Points

- **Model Location:** Project root → `models/saved_models/`
- **Model Format:** Keras 3.x format (.keras file)
- **Directory Created:** ✅ Yes (ready for model file)
- **Configuration:** ✅ Already set up in config.py
- **Required for:** Predictions via REST API

---

**Status:** Directory structure ready ✅
**Action Required:** Copy `best_model.keras` file to `models/saved_models/`
