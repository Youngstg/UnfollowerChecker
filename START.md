# 🚀 Quick Start - Instagram Unfollower Checker

## TL;DR - 3 Langkah Cepat dengan uv

```bash
# 1. Install uv (skip jika sudah install)
irm https://astral.sh/uv/install.ps1 | iex  # Windows
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac

# 2. Install dependencies
uv sync

# 3. Run!
.\dev.ps1 run   # Windows PowerShell
./dev.sh run    # Linux/Mac
```

Buka: **http://localhost:5000** 🎉

---

## 📋 Helper Scripts

### Windows (PowerShell)
```powershell
.\dev.ps1 install    # Install dependencies
.\dev.ps1 env        # Setup .env
.\dev.ps1 run        # Run app
.\dev.ps1 help       # Lihat semua command
```

### Linux/Mac
```bash
./dev.sh install    # Install dependencies
./dev.sh env        # Setup .env
./dev.sh run        # Run app
./dev.sh help       # Lihat semua command
```

---

## ⚙️ Konfigurasi

```bash
# 1. Copy template
cp .env.example .env

# 2. Edit .env
notepad .env  # Windows
nano .env     # Linux/Mac

# 3. Minimal config
FLASK_SECRET_KEY=your-random-secret-key-here
FLASK_DEBUG=True
FLASK_PORT=5000
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📖 Dokumentasi Lengkap

- **README utama**: [README.md](README.md)
- **uv Guide**: [README.uv.md](README.uv.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Installation**: [INSTALL.md](INSTALL.md)
- **Quick Tutorial**: [QUICKSTART.md](QUICKSTART.md)

---

## 🎯 Common Commands

```bash
# Development
.\dev.ps1 run              # Run development server
.\dev.ps1 prod             # Run production server

# Maintenance
.\dev.ps1 clean            # Clean cache
.\dev.ps1 db-backup        # Backup database
.\dev.ps1 format           # Format code

# Testing
.\dev.ps1 test             # Run tests
.\dev.ps1 lint             # Run linter
```

---

## 🐛 Quick Troubleshooting

### Port sudah digunakan
```bash
# Edit .env, ganti port
FLASK_PORT=8080
```

### uv command not found
```bash
# Restart terminal atau install lagi
irm https://astral.sh/uv/install.ps1 | iex
```

### Dependencies error
```bash
# Clean reinstall
rm -rf .venv
uv sync
```

### Login Error: IP Blocked / Blacklist
Lihat panduan lengkap: **[CARA_BYPASS_IP_BLOCK.md](CARA_BYPASS_IP_BLOCK.md)**

**Quick fix:**
```bash
# Generate session dari IP lain (hotspot HP/VPN)
python get_session.py

# Copy output JSON
# Lalu import di web app (tab "Import Session")
```

---

**Selamat coding! 🚀**

Butuh bantuan? Lihat [INSTALL.md](INSTALL.md), [DEPLOYMENT.md](DEPLOYMENT.md), atau [CARA_BYPASS_IP_BLOCK.md](CARA_BYPASS_IP_BLOCK.md)
