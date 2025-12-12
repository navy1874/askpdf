@echo off
REM Test GUI Import - Quick verification script

cd /d "%~dp0"

echo.
echo ======================================================================
echo   Testing GUI Import from Different Locations
echo ======================================================================
echo.

echo [Test 1] Import from project root...
python -c "from src.pdf_reader.gui import main; print('[OK] Test 1 passed')"
if errorlevel 1 (
    echo [ERROR] Test 1 failed
    goto :error
)
echo.

echo [Test 2] Import after adding path...
python -c "import sys; sys.path.insert(0, 'src/pdf_reader'); import gui; print('[OK] Test 2 passed')"
if errorlevel 1 (
    echo [ERROR] Test 2 failed
    goto :error
)
echo.

echo [Test 3] Import cli module...
cd src\pdf_reader
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd())); from cli import parse_page_ranges; print('[OK] Test 3 passed')"
if errorlevel 1 (
    echo [ERROR] Test 3 failed
    cd ..\..
    goto :error
)
cd ..\..
echo.

echo ======================================================================
echo   ALL TESTS PASSED!
echo ======================================================================
echo.
echo The GUI can now be run using:
echo   1. start_gui.bat
echo   2. python launch_gui.py
echo   3. python -m src.pdf_reader.gui
echo.
pause
exit /b 0

:error
echo.
echo ======================================================================
echo   TESTS FAILED
echo ======================================================================
echo.
pause
exit /b 1
