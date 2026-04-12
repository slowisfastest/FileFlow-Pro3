#!/usr/bin/env python3
"""创建 PyInstaller spec 文件"""
import os
from pathlib import Path

spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

# 收集 OCR 模型文件（如果存在）
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
        "pdfplumber",
        "pdf2docx",
        "PIL",
        "PIL._imagingtk",
        "PIL._tkinter_finder",
        "fitz",
        "docx",
        "openpyxl",
        "pptx",
        "reportlab",
        "reportlab.pdfbase._fontdata",
        "reportlab.pdfbase._fontdata_widths_courier",
        "reportlab.pdfbase._fontdata_widths_courierbold",
        "reportlab.pdfbase._fontdata_widths_courieroblique",
        "reportlab.pdfbase._fontdata_widths_courierboldoblique",
        "reportlab.pdfbase._fontdata_widths_helvetica",
        "reportlab.pdfbase._fontdata_widths_helveticabold",
        "reportlab.pdfbase._fontdata_widths_helveticaoblique",
        "reportlab.pdfbase._fontdata_widths_helveticaboldoblique",
        "reportlab.pdfbase._fontdata_widths_timesroman",
        "reportlab.pdfbase._fontdata_widths_timesbold",
        "reportlab.pdfbase._fontdata_widths_timesitalic",
        "reportlab.pdfbase._fontdata_widths_timesbolditalic",
        "reportlab.pdfbase._fontdata_widths_symbol",
        "reportlab.pdfbase._fontdata_widths_zapfdingbats",
        "reportlab.pdfbase._fontdata_enc_winansi",
        "reportlab.pdfbase._fontdata_enc_macroman",
        "reportlab.pdfbase._fontdata_enc_standard",
        "reportlab.pdfbase._fontdata_enc_symbol",
        "reportlab.pdfbase._fontdata_enc_zapfdingbats",
        "lxml",
        "lxml.etree",
        "lxml._elementpath",
        "xml.etree.ElementTree",
        "xml.etree.cElementTree",
        # OCR 相关依赖
        "numpy",
        "cv2",
        "paddle",
        "paddleocr",
        "skimage",
        "skimage.filters",
        "imgaug",
        "lmdb",
        "pyclipper",
        "shapely",
        "scipy",
        "easyocr",
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
    name="FileFlowPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico" if os.path.exists("icon.ico") else None,
)
'''

with open('FileFlowPro.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)
print('Spec file created successfully')
