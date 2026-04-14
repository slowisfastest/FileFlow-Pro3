#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download OCR model files for offline packaging.
Supports PaddleOCR and EasyOCR model pre-download.
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Model download directory
MODELS_DIR = Path("ocr_models")

def download_file(url: str, dest: Path, desc: str = ""):
    """Download file with progress display"""
    print(f"Downloading {desc}...")
    print(f"  URL: {url}")
    print(f"  Target: {dest}")

    dest.parent.mkdir(parents=True, exist_ok=True)

    def progress_hook(count, block_size, total_size):
        percent = min(int(count * block_size * 100 / total_size), 100)
        sys.stdout.write(f"\r  Progress: {percent}%")
        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(url, dest, reporthook=progress_hook)
        print(f"\n  [OK] Download complete")
        return True
    except Exception as e:
        print(f"\n  [FAIL] Download failed: {e}")
        return False

def download_paddleocr_models():
    """Download PaddleOCR models"""
    print("\n" + "="*60)
    print("Downloading PaddleOCR models")
    print("="*60)

    # PaddleOCR model repository
    base_url = "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese"

    models = {
        "ch_PP-OCRv4_det_infer.tar": "Detection model",
        "ch_PP-OCRv4_rec_infer.tar": "Recognition model",
        "ch_ppocr_mobile_v2.0_cls_infer.tar": "Direction classifier",
    }

    paddle_dir = MODELS_DIR / "paddleocr"
    paddle_dir.mkdir(parents=True, exist_ok=True)

    for model_file, desc in models.items():
        url = f"{base_url}/{model_file}"
        dest = paddle_dir / model_file

        if dest.exists():
            print(f"\n{desc} already exists, skipping")
            continue

        if download_file(url, dest, desc):
            print(f"  Extracting {model_file}...")
            import tarfile
            try:
                with tarfile.open(dest, 'r') as tar:
                    tar.extractall(paddle_dir)
                print(f"  [OK] Extraction complete")
                dest.unlink()
            except Exception as e:
                print(f"  [FAIL] Extraction failed: {e}")

def download_easyocr_models():
    """Download EasyOCR models"""
    print("\n" + "="*60)
    print("Downloading EasyOCR models")
    print("="*60)

    # EasyOCR models - using official GitHub releases
    # Note: EasyOCR auto-downloads models to ~/.EasyOCR/ on first run
    # Pre-download here so models can be bundled in the EXE
    base_url = "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3"

    models = [
        # (filename, description, target directory name)
        ("english_g2.zip", "English recognition model", "english_g2"),
        ("zh_sim_g2.zip", "Simplified Chinese model", "zh_sim_g2"),
    ]

    easyocr_dir = MODELS_DIR / "easyocr"
    easyocr_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    for model_file, desc, model_dir_name in models:
        dest = easyocr_dir / model_file
        model_dir = easyocr_dir / model_dir_name

        if model_dir.exists():
            print(f"\n{desc} already exists, skipping")
            success_count += 1
            continue

        if download_file(f"{base_url}/{model_file}", dest, desc):
            print(f"  Extracting {model_file}...")
            try:
                with zipfile.ZipFile(dest, 'r') as zip_ref:
                    zip_ref.extractall(easyocr_dir)
                print(f"  [OK] Extraction complete")
                dest.unlink()
                success_count += 1
            except Exception as e:
                print(f"  [FAIL] Extraction failed: {e}")

    if success_count == 0:
        print("\n  NOTE: EasyOCR models failed to pre-download.")
        print(f"  Models will be auto-downloaded on first run to ~/.EasyOCR/")
        (easyocr_dir / ".download_later").touch()

def create_model_config():
    """Create model configuration file"""
    config_content = """# OCR Model Configuration
# This file specifies offline model paths

PADDLEOCR_MODELS_DIR = "ocr_models/paddleocr"
EASYOCR_MODELS_DIR = "ocr_models/easyocr"

# Model file mapping
PADDLEOCR_DET_MODEL = "ch_PP-OCRv4_det_infer/inference.pdmodel"
PADDLEOCR_REC_MODEL = "ch_PP-OCRv4_rec_infer/inference.pdmodel"
PADDLEOCR_CLS_MODEL = "ch_ppocr_mobile_v2.0_cls_infer/inference.pdmodel"
"""

    config_path = MODELS_DIR / "models_config.py"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    print(f"\n[OK] Config created: {config_path}")

def main():
    """Main function"""
    print("="*60)
    print("OCR Model Download Tool")
    print("="*60)
    print(f"Models will be saved to: {MODELS_DIR.absolute()}")

    # Download PaddleOCR models
    download_paddleocr_models()

    # Download EasyOCR models
    download_easyocr_models()

    # Create config file
    create_model_config()

    print("\n" + "="*60)
    print("[OK] Model download complete!")
    print("="*60)
    print(f"Model directory: {MODELS_DIR.absolute()}")
    print("\nDirectory structure:")

    # Show directory structure
    for item in sorted(MODELS_DIR.rglob("*")):
        if item.is_file():
            level = len(item.relative_to(MODELS_DIR).parts) - 1
            indent = "  " * level
            print(f"{indent}|- {item.name}")

    print("\nNext steps:")
    print("1. Run build script to bundle models in the EXE")
    print("2. Or distribute ocr_models folder alongside the EXE")

if __name__ == "__main__":
    main()
