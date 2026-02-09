import shutil
import os

src = r"c:\Users\SONY\OneDrive\Desktop\brats_segmentation\best_model.keras"
dst = r"c:\Users\SONY\OneDrive\Desktop\brats_segmentation\models\saved_models\best_model.keras"

# Create destination directory if it doesn't exist
os.makedirs(os.path.dirname(dst), exist_ok=True)

shutil.copy(src, dst)
print(f"Model copied from {src} to {dst}")
print(f"File exists: {os.path.exists(dst)}")
print(f"File size: {os.path.getsize(dst) if os.path.exists(dst) else 'N/A'} bytes")
