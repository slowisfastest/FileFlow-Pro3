#!/bin/bash
# FileFlow Pro 打包脚本 (macOS) - 包含 OCR 支持
# 用法: bash build_app.sh

set -e

echo "📦 FileFlow Pro 打包中..."

# 安装 PyInstaller
echo "[1/6] 安装 PyInstaller..."
pip3 install pyinstaller --quiet

# 安装 PyTorch (CPU 版本)
echo "[2/6] 安装 PyTorch..."
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu --quiet || echo "⚠️ PyTorch 安装失败"

# 安装其他依赖
echo "[3/6] 安装依赖..."
pip3 install -r requirements.txt --quiet || echo "⚠️ 部分依赖安装失败"

# 下载 OCR 模型
echo "[4/6] 下载 OCR 模型..."
python3 download_ocr_models.py || echo "⚠️ OCR 模型下载失败，将使用在线模式"

# 创建 hooks 目录
echo "[5/6] 准备 hooks..."
mkdir -p hooks
cp hook-paddleocr.py hooks/ 2>/dev/null || true
cp hook-easyocr.py hooks/ 2>/dev/null || true

# 生成 spec 文件
echo "[6/6] 生成打包配置..."
python3 create_spec.py

# 打包
echo "🔨 开始打包..."
pyinstaller --clean --noconfirm FileFlowPro.spec

echo "✅ 打包完成！输出在 dist/FileFlowPro"

# 检查输出
if [ -f "dist/FileFlowPro" ]; then
    echo ""
    echo "📋 文件信息:"
    ls -lh dist/FileFlowPro
    echo ""
    echo "🚀 运行方式:"
    echo "   ./dist/FileFlowPro"
fi
