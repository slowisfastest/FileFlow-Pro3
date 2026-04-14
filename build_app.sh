#!/bin/bash
# FileFlow Pro 打包脚本 (macOS/Linux) - 包含 OCR 模型
# 用法: chmod +x build_app.sh && ./build_app.sh

set -e

echo "=========================================="
echo "FileFlow Pro 打包工具 (含 OCR 模型)"
echo "=========================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.11 或更高版本"
    exit 1
fi

echo "[1/6] 正在安装 PyInstaller..."
pip3 install pyinstaller -q || pip install pyinstaller -q
if [ $? -ne 0 ]; then
    echo "[错误] PyInstaller 安装失败"
    exit 1
fi
echo "    完成"

echo ""
echo "[2/6] 正在安装 PyTorch (OCR 引擎依赖)..."
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu -q || \
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu -q
if [ $? -ne 0 ]; then
    echo "[警告] PyTorch 安装失败，继续尝试..."
fi
echo "    完成"

echo ""
echo "[3/6] 正在安装其他依赖..."
pip3 install -r requirements.txt -q || pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "[警告] 部分依赖安装失败，继续尝试打包..."
fi
echo "    完成"

echo ""
echo "[4/6] 正在下载 OCR 模型..."
python3 download_ocr_models.py || python download_ocr_models.py
if [ $? -ne 0 ]; then
    echo "[警告] OCR 模型下载失败，将使用在线下载模式"
fi
# 确保 ocr_models 目录存在
mkdir -p ocr_models
echo "    完成"

echo ""
echo "[5/6] 正在生成打包配置..."
python3 create_spec.py || python create_spec.py
if [ $? -ne 0 ]; then
    echo "[错误] 生成 spec 文件失败"
    exit 1
fi
echo "    完成"

echo ""
echo "[6/6] 正在打包 FileFlow Pro..."
echo "    这可能需要 5-10 分钟，请耐心等待..."

# 创建 hooks 目录
mkdir -p hooks
cp hook-paddleocr.py hooks/ 2>/dev/null || true
cp hook-easyocr.py hooks/ 2>/dev/null || true

pyinstaller --clean --noconfirm FileFlowPro.spec

echo ""
echo "[5/5] 打包完成！"
echo ""

if [ -f "dist/FileFlowPro" ]; then
    echo "=========================================="
    echo "[成功] 可执行文件已生成！"
    echo "=========================================="
    echo ""
    echo "文件位置: dist/FileFlowPro"
    echo ""
    echo "文件大小:"
    ls -lh dist/FileFlowPro
    echo ""
    echo "功能特性:"
    echo "  - PDF 转 Word/Excel/PPT/图片/文本"
    echo "  - Word/Excel/PPT 转 PDF"
    echo "  - 图片格式转换"
    echo "  - OCR 扫描件识别 (离线可用)"
    echo ""
    echo "使用说明:"
    echo "  1. 将 dist/FileFlowPro 复制到任意位置"
    echo "  2. 双击运行即可使用"
    echo "  3. OCR 功能无需联网"
    echo ""
else
    echo "[错误] 未找到生成的可执行文件"
    echo "请检查上面的错误信息"
fi
