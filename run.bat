@echo off
REM PDF Reader Application Launcher

cd /d "%~dp0"

if exist "dist\PDFReader\PDFReader.exe" (
    echo Starting PDF Reader...
    start "" "dist\PDFReader\PDFReader.exe"
) else (
    echo [ERROR] PDFReader.exe not found
    echo Please run quick_build.bat or build.py first
    pause
    exit /b 1
)
