@echo off
REM PDF Reader - Build executable for Windows
REM Usage: build_executable.bat

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║           PDF Reader - 应用程序打包脚本 (Windows)                            ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

REM 检查 Python
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ 找到 Python %PYTHON_VERSION%
echo.

REM 检查/创建虚拟环境
echo [2/5] 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo ✅ 虚拟环境激活完成
echo.

REM 安装依赖
echo [3/5] 安装依赖包...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install PyInstaller >nul 2>&1
pip install -e . >nul 2>&1
echo ✅ 依赖安装完成
echo.

REM 清理旧的构建
echo [4/5] 清理旧的构建文件...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
echo ✅ 清理完成
echo.

REM 使用 PyInstaller 构建
echo [5/5] 构建可执行文件...
echo 运行 PyInstaller...

pyinstaller ^
    --name="PDFReader" ^
    --onedir ^
    --windowed ^
    --icon=icon.ico ^
    --add-data="src/pdf_reader;pdf_reader" ^
    --hidden-import=PyQt5 ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=pymupdf ^
    --hidden-import=pdfplumber ^
    --hidden-import=PIL ^
    --hidden-import=pypdf ^
    --collect-all PyQt5 ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    src/pdf_reader/gui.py

if exist "dist\PDFReader\PDFReader.exe" (
    echo ✅ 构建完成
    echo.
    echo ╔════════════════════════════════════════════════════════════════════════════════╗
    echo ║                          ✅ 构建成功!                                         ║
    echo ╚════════════════════════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 可执行文件位置:
    echo    Windows: dist\PDFReader\PDFReader.exe
    echo.
    echo 运行方式:
    echo    dist\PDFReader\PDFReader.exe
    echo.
    echo 快捷方式创建:
    echo    1. 右键 dist\PDFReader\PDFReader.exe
    echo    2. 选择 "创建快捷方式"
    echo    3. 移动快捷方式到桌面或开始菜单
    echo.
    pause
) else (
    echo ❌ 构建失败
    pause
    exit /b 1
)
