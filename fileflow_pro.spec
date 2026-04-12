# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
包含 OCR 模型文件的完整打包方案
"""

import sys
import os
from pathlib import Path

# 获取项目根目录
project_root = Path(SPECPATH)

# OCR 模型文件路径
ocr_models_dir = project_root / "ocr_models"

# 收集模型文件
added_files = []
if ocr_models_dir.exists():
    for root, dirs, files in os.walk(ocr_models_dir):
        for file in files:
            file_path = Path(root) / file
            # 计算相对路径
            rel_path = file_path.relative_to(project_root)
            dest_path = rel_path.parent
            added_files.append((str(file_path), str(dest_path)))

block_cipher = None

a = Analysis(
    ['fileflow_pro.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'pdf2docx',
        'pdfplumber',
        'pdfminer',
        'docx2pdf',
        'openpyxl',
        'pptx',
        'reportlab',
        'fitz',
        'PIL',
        'paddle',
        'paddleocr',
        'cv2',
        'numpy',
        'skimage',
        'skimage.filters',
        'imgaug',
        'lmdb',
        'pyclipper',
        'shapely',
        'scipy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FileFlowPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'icon.ico') if (project_root / 'icon.ico').exists() else None,
)
