@echo off
chcp 65001 > nul
echo ==========================================
echo Instagram Unfollower Checker - Instalasi
echo ==========================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python tidak terinstall!
    echo Silakan download dan install Python dari https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python terdeteksi:
python --version
echo.

REM Check if pip is installed
pip --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: pip tidak terinstall!
    echo Silakan install pip terlebih dahulu
    echo.
    pause
    exit /b 1
)

echo pip terdeteksi:
pip --version
echo.

echo Menginstall dependencies...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Instalasi gagal!
    echo Silakan cek error message di atas
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Instalasi berhasil!
echo ==========================================
echo.
echo Untuk menjalankan aplikasi:
echo 1. Double-click run.bat
echo 2. Atau ketik: python app.py
echo.
pause
