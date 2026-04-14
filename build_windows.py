#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FileFlow Pro - Windows Build Script
Run this script on Windows to generate the exe file.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if dependencies are installed"""
    print("=" * 50)
    print("FileFlow Pro - Windows Build Tool")
    print("=" * 50)
    print()

    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8+ is required")
        return False

    # Check PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found, installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully")

    return True

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

# Collect OCR model files (if exists)
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
    ['fileflow_pro.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'pdfplumber',
        'pdf2docx',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'fitz',
        'docx',
        'openpyxl',
        'pptx',
        'reportlab',
        'reportlab.pdfbase._fontdata',
        'reportlab.pdfbase._fontdata_widths_courier',
        'reportlab.pdfbase._fontdata_widths_courierbold',
        'reportlab.pdfbase._fontdata_widths_courieroblique',
        'reportlab.pdfbase._fontdata_widths_courierboldoblique',
        'reportlab.pdfbase._fontdata_widths_helvetica',
        'reportlab.pdfbase._fontdata_widths_helveticabold',
        'reportlab.pdfbase._fontdata_widths_helveticaoblique',
        'reportlab.pdfbase._fontdata_widths_helveticaboldoblique',
        'reportlab.pdfbase._fontdata_widths_timesroman',
        'reportlab.pdfbase._fontdata_widths_timesbold',
        'reportlab.pdfbase._fontdata_widths_timesitalic',
        'reportlab.pdfbase._fontdata_widths_timesbolditalic',
        'reportlab.pdfbase._fontdata_widths_symbol',
        'reportlab.pdfbase._fontdata_widths_zapfdingbats',
        'reportlab.pdfbase._fontdata_enc_winansi',
        'reportlab.pdfbase._fontdata_enc_macroman',
        'reportlab.pdfbase._fontdata_enc_standard',
        'reportlab.pdfbase._fontdata_enc_symbol',
        'reportlab.pdfbase._fontdata_enc_zapfdingbats',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'xml.etree.ElementTree',
        'xml.etree.cElementTree',
        # OCR dependencies
        'numpy',
        'cv2',
        'paddle',
        'paddleocr',
        'skimage',
        'skimage.filters',
        'imgaug',
        'lmdb',
        'pyclipper',
        'shapely',
        'scipy',
        'easyocr',
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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''

    with open('FileFlowPro.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("[OK] Spec file created")

def install_requirements():
    """Install dependencies"""
    print("\nInstalling dependencies...")

    requirements = [
        'pdfplumber>=0.10.0',
        'pdf2docx>=0.5.6',
        'Pillow>=10.0.0',
        'PyMuPDF>=1.23.0',
        'python-docx>=0.8.11',
        'openpyxl>=3.1.0',
        'python-pptx>=0.6.21',
        'reportlab>=4.0.0',
        'lxml>=4.9.0',
        'numpy>=1.24.0',
        'opencv-python>=4.8.0',
    ]

    for req in requirements:
        print(f"  Installing {req}...")
        subprocess.run([sys.executable, "-m", "pip", "install", req],
                      capture_output=True)

    # Install OCR engines (optional but recommended)
    print("\n  Installing OCR engine (PaddleOCR)...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "paddleocr>=2.7.0", "paddlepaddle>=2.5.0"],
                          capture_output=True)
    if result.returncode == 0:
        print("  [OK] PaddleOCR installed")
    else:
        print("  [WARN] PaddleOCR failed, trying EasyOCR...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "easyocr>=1.7.0"],
                              capture_output=True)
        if result.returncode == 0:
            print("  [OK] EasyOCR installed")
        else:
            print("  [WARN] EasyOCR also failed, OCR will be unavailable")

    print("[OK] Dependencies installed")

def build_exe():
    """Build exe file"""
    print("\nBuilding executable...")
    print("This may take a few minutes, please wait...")
    print()

    # Clean old builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Cleaned {folder}/")

    # Build with spec file
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "FileFlowPro.spec"
    ]

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode != 0:
        print("\n[FAIL] Build failed")
        return False

    print("\n[OK] Build succeeded!")
    return True

def copy_to_desktop():
    """Copy to desktop folder"""
    print("\nCopying to desktop...")

    # Get desktop path
    desktop = Path.home() / "Desktop"
    target_folder = desktop / "convert_for_windows_v1"

    # Create target folder
    target_folder.mkdir(exist_ok=True)

    # Copy exe file
    exe_source = Path("dist") / "FileFlowPro.exe"
    exe_target = target_folder / "FileFlowPro.exe"

    if exe_source.exists():
        shutil.copy2(exe_source, exe_target)
        print(f"[OK] Copied to: {exe_target}")

        # Create readme file
        readme = target_folder / "README.txt"
        with open(readme, 'w', encoding='utf-8') as f:
            f.write("""FileFlow Pro - File Format Converter
================================

How to use:
1. Double-click FileFlowPro.exe
2. Click "Select File" to choose a file
3. Select target format
4. Click "Start Conversion"

Supported formats:
- PDF: to Word, Excel, PPT, Image, Text
- Word: to PDF, Text
- Excel: to PDF, CSV, Text
- PPT: to PDF, Image
- Image: to PDF, convert between formats
- Text: to PDF, Word

Notes:
- First run may take a few seconds to load
- Please wait patiently for large files
- Output files are saved to desktop by default
""")
        print(f"[OK] README created: {readme}")
        return True
    else:
        print(f"[FAIL] EXE not found: {exe_source}")
        return False

def main():
    """Main function"""
    try:
        # Check dependencies
        if not check_dependencies():
            return 1

        # Install dependencies
        install_requirements()

        # Create spec file
        create_spec_file()

        # Build exe
        if not build_exe():
            return 1

        # Copy to desktop
        if not copy_to_desktop():
            return 1

        print("\n" + "=" * 50)
        print("[OK] Build complete!")
        print("=" * 50)
        print(f"\nExecutable location:")
        desktop = Path.home() / "Desktop" / "convert_for_windows_v1"
        print(f"  {desktop / 'FileFlowPro.exe'}")
        print(f"\nYou can copy this folder to any Windows PC!")

        return 0

    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
