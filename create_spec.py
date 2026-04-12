#!/usr/bin/env python3
import os
from pathlib import Path

spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

ocr_models_dir = Path("ocr_models")
added_files = []
if ocr_models_dir.exists():
    for root, dirs, files in os.walk(ocr_models_dir):
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(Path("."))
            dest_path = rel_path.parent
            added_files.append((str(file_path), str(dest_path)))

a = Analysis(
    ["fileflow_pro.py"],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        "pdfplumber", "pdf2docx", "PIL", "fitz", "docx",
        "openpyxl", "pptx", "reportlab", "lxml",
        "numpy", "cv2", "paddle", "paddleocr",
        "skimage", "skimage.filters", "imgaug",
        "lmdb", "pyclipper", "shapely", "scipy", "easyocr",
    ],
    hookspath=[], hooksconfig={}, runtime_hooks=[],
    excludes=[], win_no_prefer_redirects=False,
    win_private_assemblies=False, cipher=block_cipher, noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name="FileFlowPro", debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, upx_exclude=[], runtime_tmpdir=None,
    console=False, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None,
    icon="icon.ico" if os.path.exists("icon.ico") else None,
)
'''

with open('FileFlowPro.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)
print('Spec file created')
