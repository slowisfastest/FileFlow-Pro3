#!/usr/bin/env python3
"""
FileFlow Pro - Windows 打包脚本
在 Windows 电脑上运行此脚本生成 exe 文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    print("=" * 50)
    print("FileFlow Pro - Windows 打包工具")
    print("=" * 50)
    print()
    
    # 检查 Python 版本
    print(f"Python 版本: {sys.version}")
    if sys.version_info < (3, 8):
        print("错误: 需要 Python 3.8 或更高版本")
        return False
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller 安装完成")
    
    return True

def create_spec_file():
    """创建 PyInstaller spec 文件"""
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
        # OCR 相关依赖
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

    print("✓ 已创建 spec 文件")

def install_requirements():
    """安装依赖"""
    print("\n正在安装依赖...")
    
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
        print(f"  安装 {req}...")
        subprocess.run([sys.executable, "-m", "pip", "install", req], 
                      capture_output=True)
    
    # 安装 OCR 引擎（可选，但推荐）
    print("\n  安装 OCR 引擎 (PaddleOCR)...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "paddleocr>=2.7.0", "paddlepaddle>=2.5.0"], 
                          capture_output=True)
    if result.returncode == 0:
        print("  ✓ PaddleOCR 安装成功")
    else:
        print("  ⚠ PaddleOCR 安装失败，将尝试 EasyOCR...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "easyocr>=1.7.0"], 
                              capture_output=True)
        if result.returncode == 0:
            print("  ✓ EasyOCR 安装成功")
        else:
            print("  ⚠ EasyOCR 也安装失败，OCR 功能将不可用")
    
    print("✓ 依赖安装完成")

def build_exe():
    """构建 exe 文件"""
    print("\n正在构建可执行文件...")
    print("这可能需要几分钟时间，请耐心等待...")
    print()
    
    # 清理旧的构建
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  清理 {folder}/")
    
    # 使用 spec 文件构建
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "FileFlowPro.spec"
    ]
    
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode != 0:
        print("\n✗ 构建失败")
        return False
    
    print("\n✓ 构建成功!")
    return True

def copy_to_desktop():
    """复制到桌面文件夹"""
    print("\n正在复制到桌面...")
    
    # 获取桌面路径
    desktop = Path.home() / "Desktop"
    target_folder = desktop / "convert_for_windows_v1"
    
    # 创建目标文件夹
    target_folder.mkdir(exist_ok=True)
    
    # 复制 exe 文件
    exe_source = Path("dist") / "FileFlowPro.exe"
    exe_target = target_folder / "FileFlowPro.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_target)
        print(f"✓ 已复制到: {exe_target}")
        
        # 创建说明文件
        readme = target_folder / "使用说明.txt"
        with open(readme, 'w', encoding='utf-8') as f:
            f.write("""FileFlow Pro - 文件格式转换工具
================================

使用方法:
1. 双击 FileFlowPro.exe 运行程序
2. 点击"选择文件"选择要转换的文件
3. 选择目标格式
4. 点击"开始转换"

支持的格式:
- PDF: 可转 Word, Excel, PPT, 图片, 文本
- Word: 可转 PDF, 文本
- Excel: 可转 PDF, CSV, 文本
- PPT: 可转 PDF, 图片
- 图片: 可转 PDF, 互相转换
- 文本: 可转 PDF, Word

注意事项:
- 首次运行可能需要几秒钟加载
- 转换大文件时请耐心等待
- 输出文件默认保存在桌面

如有问题，请联系开发者。
""")
        print(f"✓ 已创建使用说明: {readme}")
        return True
    else:
        print(f"✗ 未找到 exe 文件: {exe_source}")
        return False

def main():
    """主函数"""
    try:
        # 检查依赖
        if not check_dependencies():
            return 1
        
        # 安装依赖
        install_requirements()
        
        # 创建 spec 文件
        create_spec_file()
        
        # 构建 exe
        if not build_exe():
            return 1
        
        # 复制到桌面
        if not copy_to_desktop():
            return 1
        
        print("\n" + "=" * 50)
        print("打包完成!")
        print("=" * 50)
        print(f"\n可执行文件位置:")
        desktop = Path.home() / "Desktop" / "convert_for_windows_v1"
        print(f"  {desktop / 'FileFlowPro.exe'}")
        print(f"\n可以直接将此文件夹复制到 Windows 电脑使用!")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
