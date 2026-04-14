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

echo [1/6] 正在安装 PyInstaller...
pip install pyinstaller -q
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败
    pause
    exit /b 1
)
echo     完成

echo.
echo [2/6] 正在安装 PyTorch...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu -q
if errorlevel 1 (
    echo [警告] PyTorch 安装失败，OCR 功能可能不可用
)
echo     完成

echo.
echo [3/6] 正在安装其他依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [警告] 部分依赖安装失败，继续尝试打包...
)
echo     完成

echo.
echo [4/6] 正在下载 OCR 模型...
python download_ocr_models.py
if errorlevel 1 (
    echo [警告] OCR 模型下载失败，将使用在线下载模式
)
echo     完成

echo.
echo [5/6] 正在打包 FileFlow Pro...
echo     这可能需要 5-10 分钟，请耐心等待...

REM 创建 hooks 目录并复制 hook 文件
if not exist "hooks" mkdir hooks
copy "hook-paddleocr.py" "hooks\hook-paddleocr.py" >nul 2>&1
copy "hook-easyocr.py" "hooks\hook-easyocr.py" >nul 2>&1

REM 生成 spec 文件
python create_spec.py
if errorlevel 1 (
    echo [错误] 生成 spec 文件失败
    pause
    exit /b 1
)

REM 使用生成的 spec 文件打包
pyinstaller --clean --noconfirm FileFlowPro.spec

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
        --hidden-import "torch" ^
        --hidden-import "torchvision" ^
        --hidden-import "scipy" ^
        --hidden-import "shapely" ^
        --hidden-import "easyocr" ^
        fileflow_pro.py
)

echo.
echo [6/6] 打包完成！
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
