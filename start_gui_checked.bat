@echo off
REM PDF Reader - GUI Start with Dependency Check

cd /d "%~dp0"

echo ======================================================================
echo   PDF Reader - Starting with dependency verification
echo ======================================================================
echo.

REM Check dependencies (show output)
echo [1/2] Checking dependencies...
python check_dependencies.py
if errorlevel 1 (
    echo.
    echo [ERROR] Some dependencies are missing!
    echo.
    echo Please run: install_dependencies.bat
    echo.
    pause
    exit /b 1
)

echo.
echo [2/2] Starting PDF Reader...
echo.
python launch_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    echo.
    pause
    exit /b 1
)

exit /b 0
