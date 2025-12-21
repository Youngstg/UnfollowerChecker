# Instagram Unfollower Checker - Quick Start dengan uv ⚡

Web app modern untuk tracking Instagram unfollowers dengan deployment super cepat menggunakan **uv**.

## ⚡ Quick Start (3 Langkah!)

### 1. Install uv

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Setup Project

```bash
# Clone/masuk ke folder project
cd d:\UnfollowerChecker

# Install dependencies (SUPER CEPAT - 10x lebih cepat dari pip!)
uv sync

# Copy environment template
cp .env.example .env
```

### 3. Run!

```bash
# Aktivasi virtual environment
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Jalankan aplikasi
python app.py
```

Buka browser: **http://localhost:5000** 🎉

---

## 🎯 Kenapa Pakai uv?

| Fitur | pip | uv |
|-------|-----|-----|
| Kecepatan install | Lambat (1-2 menit) | **Super cepat (5-10 detik)** |
| Virtual env | Manual setup | Otomatis |
| Dependency resolution | Sering conflict | Smart resolution |
| Lock file | requirements.txt | pyproject.toml + uv.lock |
| Caching | Basic | Advanced caching |

---

## 📦 Command Cheatsheet

### Setup & Install
```bash
# Install dependencies
uv sync

# Install package baru
uv add flask-cors

# Install dev dependencies
uv add --dev pytest black

# Update semua packages
uv lock --upgrade
uv sync
```

### Virtual Environment
```bash
# Buat venv (otomatis dengan uv sync)
uv venv

# Buat venv dengan Python version tertentu
uv venv --python 3.11

# Aktivasi venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### Run Commands
```bash
# Run tanpa aktivasi venv
uv run python app.py

# Run dengan gunicorn (production)
uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run tests
uv run pytest

# Format code
uv run black .
```

---

## 🔧 Konfigurasi (.env)

```bash
# Edit .env file
notepad .env  # Windows
nano .env     # Linux/Mac
```

Isi minimal:
```env
FLASK_SECRET_KEY=ganti-dengan-random-string-panjang
FLASK_DEBUG=True
FLASK_PORT=5000
```

Generate secret key:
```bash
# Windows
python -c "import secrets; print(secrets.token_hex(32))"

# Linux/Mac
uv run python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Deployment

### Development
```bash
# Run dengan auto-reload
uv run python app.py
```

### Production
```bash
# Run dengan gunicorn (4 workers)
uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Dengan lebih banyak workers
uv run gunicorn -w 8 --threads 2 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
# Build
docker build -t unfollower-checker .

# Run
docker run -p 5000:5000 --env-file .env unfollower-checker
```

**Lihat [DEPLOYMENT.md](DEPLOYMENT.md) untuk deployment lengkap!**

---

## 📁 Struktur Project

```
UnfollowerChecker/
├── app.py                    # Main application
├── pyproject.toml           # Dependencies & config
├── .env.example             # Environment template
├── .env                     # Your config (JANGAN commit!)
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── unfollower_tracker.db   # SQLite database
└── .venv/                   # Virtual environment (auto-created)
```

---

## 🐛 Troubleshooting

### "uv: command not found"
```bash
# Restart terminal atau:
# Windows
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine")

# Linux/Mac
source ~/.bashrc  # atau ~/.zshrc
```

### "Virtual environment not activated"
```bash
# Aktivasi manual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Atau gunakan uv run (tidak perlu aktivasi)
uv run python app.py
```

### "Port 5000 already in use"
```bash
# Edit .env
FLASK_PORT=8080

# Atau kill process di port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Dependencies tidak terinstall
```bash
# Clean install
rm -rf .venv
uv sync

# Atau reinstall
uv sync --reinstall
```

---

## 🎓 Tutorial Lengkap

### First Time Setup
```bash
# 1. Install uv
irm https://astral.sh/uv/install.ps1 | iex  # Windows

# 2. Clone project
cd d:\UnfollowerChecker

# 3. Install dependencies
uv sync

# 4. Setup environment
cp .env.example .env
notepad .env  # Edit konfigurasi

# 5. Run!
.venv\Scripts\activate
python app.py
```

### Daily Development
```bash
# Aktivasi venv
.venv\Scripts\activate

# Run app
python app.py

# Atau tanpa aktivasi:
uv run python app.py
```

### Adding New Features
```bash
# Install package baru
uv add requests flask-cors

# Install dev tools
uv add --dev pytest black flake8

# Update dependencies
uv lock --upgrade
uv sync
```

---

## 📚 Resources

- **uv Docs**: https://docs.astral.sh/uv/
- **Project README**: [README.md](README.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Installation Help**: [INSTALL.md](INSTALL.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

---

## ⚙️ Advanced Tips

### Faster Installs
```bash
# Use system Python (skip venv creation)
uv pip install -r requirements.txt --system

# Parallel downloads
uv sync --no-cache
```

### Lock Dependencies
```bash
# Create lock file
uv lock

# Install from lock
uv sync --frozen

# Update lock
uv lock --upgrade
```

### Multiple Python Versions
```bash
# Use specific Python
uv venv --python 3.11
uv venv --python 3.9

# List available Pythons
uv python list
```

---

## 🎯 Next Steps

1. ✅ Install uv
2. ✅ Run `uv sync`
3. ✅ Copy `.env.example` ke `.env`
4. ✅ Run `python app.py`
5. 🌐 Deploy ke production (lihat [DEPLOYMENT.md](DEPLOYMENT.md))

---

**Selamat coding! 🚀**

Jika ada masalah, cek [INSTALL.md](INSTALL.md) atau buat issue!
