@echo off
REM PDF Reader - GUI Quick Start Script

cd /d "%~dp0"

REM Check if venv exists and use it, otherwise use global Python
if exist "venv\Scripts\python.exe" (
    echo Using virtual environment...
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    echo Using global Python...
    set PYTHON_CMD=python
)

REM Start GUI
echo Starting PDF Reader...
echo.
%PYTHON_CMD% launch_gui.py

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo [ERROR] Application failed to start
    echo ======================================================================
    echo.
    echo This usually means PyQt5 or other dependencies are missing.
    echo.
    echo Quick fix - Install dependencies now? (Y/N)
    choice /C YN /N /M "Press Y to install, N to exit: "
    if errorlevel 2 goto :end
    if errorlevel 1 goto :install
)

exit /b 0

:install
echo.
echo Installing dependencies...
%PYTHON_CMD% -m pip install PyQt5 pymupdf pdfplumber pypdf Pillow typer rich
if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)
echo.
echo [OK] Dependencies installed! Starting application...
echo.
%PYTHON_CMD% launch_gui.py
pause
exit /b 0

:end
pause
exit /b 1
