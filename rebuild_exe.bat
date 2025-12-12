@echo off
REM Rebuild PDFReader.exe with all dependencies

cd /d "%~dp0"

echo.
echo ======================================================================
echo   Rebuilding PDFReader.exe with PyQt5 dependencies
echo ======================================================================
echo.

echo Cleaning old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "PDFReader.spec" del /q "PDFReader.spec"
echo Done.
echo.

echo Starting PyInstaller build (this will take 2-5 minutes)...
echo Please wait and DO NOT interrupt...
echo.

venv\Scripts\python.exe -m PyInstaller ^
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

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo   Build Complete!
echo ======================================================================
echo.
echo Executable location: dist\PDFReader\PDFReader.exe
echo.
echo Testing if PyQt5 is included...
dir /s /b dist\PDFReader\_internal\PyQt5* | findstr /i "PyQt5"
if errorlevel 1 (
    echo [WARNING] PyQt5 files not found in build
) else (
    echo [OK] PyQt5 files found in build
)
echo.
pause
