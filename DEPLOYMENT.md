# Deployment Guide - Instagram Unfollower Checker

Panduan deployment modern menggunakan **uv** (ultra-fast Python package installer).

## 🚀 Quick Start dengan uv

### 1. Install uv

#### Windows (PowerShell)
```powershell
# Install uv
irm https://astral.sh/uv/install.ps1 | iex

# Atau dengan pipx
pipx install uv
```

#### Linux/Mac
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Atau dengan pip
pip install uv
```

### 2. Clone/Download Project
```bash
cd d:\UnfollowerChecker
```

### 3. Setup Environment & Install Dependencies

```bash
# Buat virtual environment dan install dependencies (SUPER CEPAT!)
uv sync

# Atau manual:
uv venv
uv pip install -e .
```

### 4. Setup Environment Variables

```bash
# Copy template .env
cp .env.example .env

# Edit .env dengan text editor
# Windows: notepad .env
# Linux/Mac: nano .env
```

Edit `.env`:
```env
FLASK_SECRET_KEY=ganti-dengan-random-string-panjang-disini
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DATABASE_URI=sqlite:///unfollower_tracker.db
```

### 5. Run Application

```bash
# Aktivasi virtual environment (otomatis dengan uv)
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Jalankan aplikasi
python app.py
```

Buka browser: **http://localhost:5000**

---

## 📋 Cara Pakai uv

### Install Dependencies
```bash
# Install semua dependencies dari pyproject.toml
uv sync

# Install package tertentu
uv pip install flask

# Install dev dependencies
uv sync --extra dev

# Update dependencies
uv pip install --upgrade -r pyproject.toml
```

### Virtual Environment
```bash
# Buat venv
uv venv

# Buat venv dengan Python version tertentu
uv venv --python 3.11

# Aktivasi venv
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# Deaktivasi
deactivate
```

### Run Commands
```bash
# Run dengan uv (otomatis menggunakan venv)
uv run python app.py

# Run script lain
uv run pytest
uv run black .
```

---

## 🐳 Docker Deployment (Optional)

Buat `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Install dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 5000

# Run app
CMD ["uv", "run", "python", "app.py"]
```

Build & Run:
```bash
# Build image
docker build -t unfollower-checker .

# Run container
docker run -p 5000:5000 --env-file .env unfollower-checker
```

---

## 🌐 Production Deployment

### 1. Setup untuk Production

Edit `.env`:
```env
FLASK_SECRET_KEY=super-secret-random-string-min-32-chars
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DATABASE_URI=sqlite:///unfollower_tracker.db
```

### 2. Install Production Server (Gunicorn)

Tambahkan ke `pyproject.toml`:
```toml
dependencies = [
    "flask>=3.0.0",
    "flask-sqlalchemy>=3.1.1",
    "instagrapi>=2.1.2",
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
    "gunicorn>=21.0.0",  # Production server
]
```

Install:
```bash
uv sync
```

### 3. Run dengan Gunicorn

```bash
# Aktivasi venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run dengan gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Atau dengan uv
uv run gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 4. Setup Systemd Service (Linux)

Buat `/etc/systemd/system/unfollower-checker.service`:

```ini
[Unit]
Description=Instagram Unfollower Checker
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/UnfollowerChecker
Environment="PATH=/path/to/UnfollowerChecker/.venv/bin"
ExecStart=/path/to/UnfollowerChecker/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl enable unfollower-checker
sudo systemctl start unfollower-checker
sudo systemctl status unfollower-checker
```

### 5. Nginx Reverse Proxy

Install nginx:
```bash
sudo apt install nginx
```

Konfigurasi `/etc/nginx/sites-available/unfollower-checker`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/UnfollowerChecker/static;
        expires 30d;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/unfollower-checker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL dengan Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_SECRET_KEY` | dev-secret-key | Secret key untuk session (WAJIB diganti di production) |
| `FLASK_DEBUG` | True | Debug mode (False untuk production) |
| `FLASK_HOST` | 0.0.0.0 | Host untuk bind |
| `FLASK_PORT` | 5000 | Port aplikasi |
| `DATABASE_URI` | sqlite:///unfollower_tracker.db | Database connection string |

---

## 📦 Platform Deployment

### Render.com

1. Fork/upload repo ke GitHub
2. Buat Web Service di Render
3. Set build command: `uv sync`
4. Set start command: `uv run gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
5. Add environment variables dari `.env.example`

### Railway.app

1. Connect GitHub repo
2. Railway otomatis detect Python
3. Add environment variables
4. Deploy!

### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create unfollower-checker
heroku config:set FLASK_SECRET_KEY=your-secret-key
git push heroku main
```

### DigitalOcean App Platform

1. Create App dari GitHub
2. Set build command: `uv sync`
3. Set run command: `uv run gunicorn -w 4 -b 0.0.0.0:8080 app:app`
4. Add environment variables

---

## 🔒 Security Checklist

- [ ] Ganti `FLASK_SECRET_KEY` dengan random string
- [ ] Set `FLASK_DEBUG=False` di production
- [ ] Jangan commit file `.env` ke git
- [ ] Gunakan HTTPS (SSL/TLS)
- [ ] Setup firewall
- [ ] Regular backup database
- [ ] Rate limiting untuk Instagram API
- [ ] Update dependencies secara berkala

---

## 📊 Monitoring & Maintenance

### Logs
```bash
# Systemd logs
sudo journalctl -u unfollower-checker -f

# Application logs
tail -f /var/log/unfollower-checker.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Database Backup
```bash
# Backup SQLite database
cp unfollower_tracker.db unfollower_tracker.db.backup

# Scheduled backup (crontab)
0 2 * * * cp /path/to/unfollower_tracker.db /path/to/backups/unfollower_tracker.db.$(date +\%Y\%m\%d)
```

### Update Application
```bash
# Pull latest code
git pull

# Update dependencies
uv sync

# Restart service
sudo systemctl restart unfollower-checker
```

---

## 🐛 Troubleshooting

### uv tidak terinstall
```bash
# Windows
irm https://astral.sh/uv/install.ps1 | iex

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Virtual environment tidak aktif
```bash
# Aktifkan manual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Atau gunakan uv run
uv run python app.py
```

### Port already in use
```bash
# Ganti port di .env
FLASK_PORT=8080
```

### Database locked
```bash
# Stop semua instance aplikasi
# Restart aplikasi
```

---

## 🚀 Performance Tips

1. **Gunakan Gunicorn** dengan multiple workers
2. **Enable caching** untuk static files
3. **Database optimization**: Regular vacuum SQLite
4. **Rate limiting**: Batasi request ke Instagram API
5. **CDN**: Gunakan CDN untuk static assets

---

## 📚 References

- [uv Documentation](https://docs.astral.sh/uv/)
- [Flask Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

Selamat deploy! 🎉
