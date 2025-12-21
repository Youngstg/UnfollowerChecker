@echo off
chcp 65001 > nul
echo ==========================================
echo Instagram Unfollower Checker
echo ==========================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak terinstall!
    echo Silakan jalankan install.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask" > nul 2>&1
if errorlevel 1 (
    echo ERROR: Dependencies belum terinstall!
    echo Silakan jalankan install.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

echo Memulai aplikasi...
echo.
echo ==========================================
echo Buka browser dan akses:
echo.
echo    http://localhost:5000
echo.
echo ==========================================
echo.
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ERROR: Aplikasi berhenti dengan error!
    echo Silakan cek error message di atas
    echo.
)

pause
