# Panduan Instalasi Lengkap

## Metode 1: Instalasi Otomatis (Windows)

### Langkah 1: Install Dependencies
```bash
# Double-click file ini:
install.bat
```

### Langkah 2: Jalankan Aplikasi
```bash
# Double-click file ini:
run.bat
```

---

## Metode 2: Instalasi Manual

### Prasyarat
1. **Python 3.8 atau lebih tinggi**
   - Download dari: https://www.python.org/downloads/
   - Saat install, centang "Add Python to PATH"

2. **pip** (biasanya sudah terinstall dengan Python)

### Langkah Instalasi

#### 1. Cek Python dan pip
```bash
# Buka Command Prompt atau Terminal
# Cek Python
python --version

# Cek pip
pip --version
```

Jika ada error, pastikan Python sudah terinstall dan ada di PATH.

#### 2. Install Dependencies
```bash
# Masuk ke folder project
cd d:\UnfollowerChecker

# Update pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 3. Jalankan Aplikasi
```bash
python app.py
```

#### 4. Buka Browser
```
http://localhost:5000
```

---

## Troubleshooting Instalasi

### Error: "Python tidak terinstall"

**Solusi:**
1. Download Python dari https://www.python.org/downloads/
2. Install dengan centang "Add Python to PATH"
3. Restart Command Prompt
4. Coba lagi

### Error: "pip tidak terinstall"

**Solusi:**
```bash
# Download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip
python get-pip.py
```

### Error: "No module named 'flask'"

**Solusi:**
```bash
# Install manual satu per satu
pip install Flask
pip install Flask-SQLAlchemy
pip install instagrapi
pip install requests
```

### Error: "Permission denied"

**Solusi:**
```bash
# Jalankan Command Prompt sebagai Administrator
# Atau gunakan --user flag
pip install --user -r requirements.txt
```

### Error: "SSL Certificate Error"

**Solusi:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Error: "Microsoft Visual C++ required"

**Solusi:**
1. Download dan install Microsoft Visual C++ Build Tools
2. Link: https://visualstudio.microsoft.com/visual-cpp-build-tools/
3. Install "Desktop development with C++"
4. Restart dan coba install lagi

---

## Verifikasi Instalasi

Setelah instalasi, cek apakah semua module terinstall:

```bash
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import flask_sqlalchemy; print('SQLAlchemy: OK')"
python -c "import instagrapi; print('Instagrapi: OK')"
python -c "import requests; print('Requests:', requests.__version__)"
```

Jika semua OK, instalasi berhasil!

---

## Instalasi di Linux/Mac

### 1. Install Python dan pip
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Mac (dengan Homebrew)
brew install python3
```

### 2. Install Dependencies
```bash
cd /path/to/UnfollowerChecker
pip3 install -r requirements.txt
```

### 3. Jalankan Aplikasi
```bash
python3 app.py
```

---

## Virtual Environment (Recommended)

Menggunakan virtual environment untuk isolasi dependencies:

### Windows
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan app
python app.py

# Deaktivasi (setelah selesai)
deactivate
```

### Linux/Mac
```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Jalankan app
python app.py

# Deaktivasi (setelah selesai)
deactivate
```

---

## Alternatif: Instalasi dengan Anaconda

Jika menggunakan Anaconda:

```bash
# Buat environment baru
conda create -n unfollower python=3.10

# Aktifkan environment
conda activate unfollower

# Install dependencies
pip install -r requirements.txt

# Jalankan app
python app.py
```

---

## Masalah Umum Lainnya

### Port 5000 sudah digunakan

**Solusi:** Edit [app.py](app.py) baris terakhir:
```python
# Ganti 5000 dengan port lain, misal 8080
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Firewall Blocking

**Solusi:**
1. Buka Windows Firewall
2. Allow Python melalui firewall
3. Atau akses dengan http://127.0.0.1:5000

### Browser tidak bisa akses

**Solusi:**
1. Pastikan aplikasi running (tidak ada error)
2. Coba http://127.0.0.1:5000 atau http://0.0.0.0:5000
3. Clear browser cache
4. Coba browser lain

---

## Dependencies Detail

File `requirements.txt` berisi:
- **Flask**: Web framework untuk Python
- **Flask-SQLAlchemy**: ORM untuk database
- **instagrapi**: Library untuk Instagram API
- **requests**: HTTP library

Total size: ~50-100 MB

---

## Update Dependencies

Jika ingin update ke versi terbaru:

```bash
pip install --upgrade -r requirements.txt
```

---

## Kontak Support

Jika masih ada masalah setelah mencoba semua solusi di atas, silakan:
1. Screenshot error message
2. Copy paste error log
3. Buat issue di repository
4. Atau hubungi developer

---

Selamat menggunakan Instagram Unfollower Checker!
