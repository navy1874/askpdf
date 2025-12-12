@echo off
REM Quick Build PDF Reader Executable (Windows)

cd /d "%~dp0"

echo.
echo ======================================================================
echo   PDF Reader - Windows Build
echo ======================================================================
echo.

REM Determine which Python to use
if exist "venv\Scripts\python.exe" (
    echo Using virtual environment Python...
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    echo Using global Python...
    set PYTHON_CMD=python
)
echo.

echo [1/3] Installing PyInstaller...
%PYTHON_CMD% -m pip install PyInstaller -q
if errorlevel 1 (
    echo [ERROR] PyInstaller installation failed
    pause
    exit /b 1
)
echo [OK] Done
echo.

echo [2/3] Cleaning old files...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
echo [OK] Done
echo.

echo [3/3] Building executable...
echo This may take several minutes...
echo.
%PYTHON_CMD% -m PyInstaller ^
    --clean ^
    --name=PDFReader ^
    --onedir ^
    --windowed ^
    --icon=icon.ico ^
    --add-data="icon.ico;." ^
    --add-data="src/pdf_reader;pdf_reader" ^
    --hidden-import=PyQt5 ^
    --hidden-import=PyQt5.QtCore ^
    --hidden-import=PyQt5.QtGui ^
    --hidden-import=PyQt5.QtWidgets ^
    --hidden-import=pymupdf ^
    --hidden-import=pdfplumber ^
    --hidden-import=PIL ^
    --hidden-import=pypdf ^
    --collect-all=PyQt5 ^
    --exclude-module=matplotlib ^
    --exclude-module=numpy ^
    --exclude-module=pandas ^
    --exclude-module=scipy ^
    src/pdf_reader/gui.py

if exist "dist\PDFReader\PDFReader.exe" (
    echo.
    echo ======================================================================
    echo   BUILD SUCCESSFUL!
    echo ======================================================================
    echo.
    echo Executable: dist\PDFReader\PDFReader.exe
    echo.
    echo How to run:
    echo   1. Double-click: dist\PDFReader\PDFReader.exe
    echo   2. Command line: dist\PDFReader\PDFReader.exe
    echo.
    pause
) else (
    echo.
    echo [ERROR] Build failed - executable not generated
    echo.
    pause
    exit /b 1
)
