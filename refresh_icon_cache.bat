@echo off
REM Refresh Windows Icon Cache

echo Clearing Windows icon cache...
echo.

taskkill /f /im explorer.exe

timeout /t 2 /nobreak >nul

cd /d %userprofile%\AppData\Local
attrib -h IconCache.db
del IconCache.db
attrib -h Microsoft\Windows\Explorer\iconcache*.db
del Microsoft\Windows\Explorer\iconcache*.db

start explorer.exe

echo.
echo Icon cache cleared! Please check your executable now.
echo.
pause
