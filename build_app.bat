@echo off
REM FileFlow Pro 打包脚本 (Windows) - 包含 OCR 模型
REM 用法: 双击运行 build_app.bat

echo ==========================================
echo FileFlow Pro 打包工具 (含 OCR 模型)
echo ==========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.11 或更高版本
    pause
    exit /b 1
)

echo [1/5] 正在安装 PyInstaller...
pip install pyinstaller -q
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败
    pause
    exit /b 1
)
echo     完成

echo.
echo [2/5] 正在安装依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [警告] 部分依赖安装失败，继续尝试打包...
)
echo     完成

echo.
echo [3/5] 正在下载 OCR 模型...
python download_ocr_models.py
if errorlevel 1 (
    echo [警告] OCR 模型下载失败，将使用在线下载模式
)
echo     完成

echo.
echo [4/5] 正在打包 FileFlow Pro...
echo     这可能需要 5-10 分钟，请耐心等待...

pyinstaller --clean fileflow_pro.spec

if errorlevel 1 (
    echo.
    echo [错误] 打包失败，尝试使用命令行模式...
    echo.
    pyinstaller ^
        --name "FileFlowPro" ^
        --onefile ^
        --windowed ^
        --add-data "ocr_models;ocr_models" ^
        --hidden-import "pdf2docx" ^
        --hidden-import "pdfplumber" ^
        --hidden-import "pdfminer" ^
        --hidden-import "docx2pdf" ^
        --hidden-import "openpyxl" ^
        --hidden-import "pptx" ^
        --hidden-import "reportlab" ^
        --hidden-import "fitz" ^
        --hidden-import "PIL" ^
        --hidden-import "paddle" ^
        --hidden-import "paddleocr" ^
        --hidden-import "cv2" ^
        --hidden-import "numpy" ^
        --hidden-import "skimage" ^
        --hidden-import "skimage.filters" ^
        --hidden-import "imgaug" ^
        --hidden-import "lmdb" ^
        --hidden-import "pyclipper" ^
        fileflow_pro.py
)

echo.
echo [5/5] 打包完成！
echo.

if exist "dist\FileFlowPro.exe" (
    echo ==========================================
    echo [成功] EXE 文件已生成！
    echo ==========================================
    echo.
    echo 文件位置: dist\FileFlowPro.exe
    echo.
    echo 文件大小:
    dir "dist\FileFlowPro.exe" | findstr "FileFlowPro.exe"
    echo.
    echo 功能特性:
    echo   - PDF 转 Word/Excel/PPT/图片/文本
    echo   - Word/Excel/PPT 转 PDF
    echo   - 图片格式转换
    echo   - OCR 扫描件识别 (离线可用)
    echo.
    echo 使用说明:
    echo   1. 将 dist\FileFlowPro.exe 复制到任意位置
    echo   2. 双击运行即可使用
    echo   3. OCR 功能无需联网
    echo.
) else (
    echo [错误] 未找到生成的 EXE 文件
    echo 请检查上面的错误信息
)

pause
