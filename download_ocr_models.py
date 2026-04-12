#!/usr/bin/env python3
"""
下载 OCR 模型文件用于离线打包
支持 PaddleOCR 和 EasyOCR 模型预下载
"""

import os
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path

# 模型下载目录
MODELS_DIR = Path("ocr_models")

def download_file(url: str, dest: Path, desc: str = ""):
    """下载文件并显示进度"""
    print(f"下载 {desc}...")
    print(f"  URL: {url}")
    print(f"  目标: {dest}")
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    def progress_hook(count, block_size, total_size):
        percent = min(int(count * block_size * 100 / total_size), 100)
        sys.stdout.write(f"\r  进度: {percent}%")
        sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, dest, reporthook=progress_hook)
        print(f"\n  ✓ 下载完成")
        return True
    except Exception as e:
        print(f"\n  ✗ 下载失败: {e}")
        return False

def download_paddleocr_models():
    """下载 PaddleOCR 模型"""
    print("\n" + "="*60)
    print("下载 PaddleOCR 模型")
    print("="*60)
    
    # PaddleOCR 模型仓库
    base_url = "https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese"
    
    models = {
        "ch_PP-OCRv4_det_infer.tar": "检测模型",
        "ch_PP-OCRv4_rec_infer.tar": "识别模型",
        "ch_ppocr_mobile_v2.0_cls_infer.tar": "方向分类模型",
    }
    
    paddle_dir = MODELS_DIR / "paddleocr"
    paddle_dir.mkdir(parents=True, exist_ok=True)
    
    for model_file, desc in models.items():
        url = f"{base_url}/{model_file}"
        dest = paddle_dir / model_file
        
        if dest.exists():
            print(f"\n{desc} 已存在，跳过")
            continue
        
        if download_file(url, dest, desc):
            # 解压 tar 文件
            print(f"  解压 {model_file}...")
            import tarfile
            try:
                with tarfile.open(dest, 'r') as tar:
                    tar.extractall(paddle_dir)
                print(f"  ✓ 解压完成")
                # 删除 tar 文件节省空间
                dest.unlink()
            except Exception as e:
                print(f"  ✗ 解压失败: {e}")

def download_easyocr_models():
    """下载 EasyOCR 模型"""
    print("\n" + "="*60)
    print("下载 EasyOCR 模型")
    print("="*60)
    
    # EasyOCR 模型仓库
    base_url = "https://github.com/JaidedAI/EasyOCR/releases/download/v1.3"
    
    models = {
        "english_g2.zip": "英文识别模型",
        "zh_sim_g2.zip": "简体中文识别模型",
    }
    
    easyocr_dir = MODELS_DIR / "easyocr"
    easyocr_dir.mkdir(parents=True, exist_ok=True)
    
    for model_file, desc in models.items():
        url = f"{base_url}/{model_file}"
        dest = easyocr_dir / model_file
        
        if dest.exists():
            print(f"\n{desc} 已存在，跳过")
            continue
        
        if download_file(url, dest, desc):
            # 解压 zip 文件
            print(f"  解压 {model_file}...")
            try:
                with zipfile.ZipFile(dest, 'r') as zip_ref:
                    zip_ref.extractall(easyocr_dir)
                print(f"  ✓ 解压完成")
                # 删除 zip 文件节省空间
                dest.unlink()
            except Exception as e:
                print(f"  ✗ 解压失败: {e}")

def create_model_config():
    """创建模型配置文件"""
    config_content = """# OCR 模型配置
# 此文件用于指定离线模型路径

PADDLEOCR_MODELS_DIR = "ocr_models/paddleocr"
EASYOCR_MODELS_DIR = "ocr_models/easyocr"

# 模型文件映射
PADDLEOCR_DET_MODEL = "ch_PP-OCRv4_det_infer/inference.pdmodel"
PADDLEOCR_REC_MODEL = "ch_PP-OCRv4_rec_infer/inference.pdmodel"
PADDLEOCR_CLS_MODEL = "ch_ppocr_mobile_v2.0_cls_infer/inference.pdmodel"
"""
    
    config_path = MODELS_DIR / "models_config.py"
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    print(f"\n✓ 配置文件已创建: {config_path}")

def main():
    """主函数"""
    print("="*60)
    print("OCR 模型下载工具")
    print("="*60)
    print(f"模型将下载到: {MODELS_DIR.absolute()}")
    
    # 下载 PaddleOCR 模型
    download_paddleocr_models()
    
    # 下载 EasyOCR 模型
    download_easyocr_models()
    
    # 创建配置文件
    create_model_config()
    
    print("\n" + "="*60)
    print("模型下载完成！")
    print("="*60)
    print(f"模型目录: {MODELS_DIR.absolute()}")
    print("\n目录结构:")
    
    # 显示目录结构
    for item in sorted(MODELS_DIR.rglob("*")):
        if item.is_file():
            level = len(item.relative_to(MODELS_DIR).parts) - 1
            indent = "  " * level
            print(f"{indent}├── {item.name}")
    
    print("\n下一步:")
    print("1. 运行打包脚本将模型包含在 EXE 中")
    print("2. 或者将 ocr_models 目录与 EXE 一起分发")

if __name__ == "__main__":
    main()
