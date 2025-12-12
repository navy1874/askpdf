@echo off
REM PDF Reader - Dependencies Installation Script

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo   PDF Reader - Dependencies Installer
echo ======================================================================
echo.

REM Check Python
echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Upgrade pip
echo [2/3] Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo [3/3] Installing project dependencies...
python -m pip install PyQt5 pymupdf pdfplumber pypdf Pillow typer rich
if errorlevel 1 (
    echo [ERROR] Dependencies installation failed
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Verify installation
echo Verifying installation...
python check_dependencies.py
if errorlevel 1 (
    echo [ERROR] Installation verification failed
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   ALL DEPENDENCIES INSTALLED!
echo ======================================================================
echo.
echo You can now:
echo   1. Run GUI: python launch_gui.py
echo   2. Run GUI: start_gui.bat
echo   3. Run CLI: python -m pdf_reader.cli --help
echo   4. Launch app: run.bat
echo.
pause
