# 🚂 Deployment ke Railway

Panduan lengkap deploy Instagram Unfollower Checker ke Railway.

## 📋 Prerequisites

1. Akun GitHub (untuk connect repository)
2. Akun Railway (gratis: https://railway.app)
3. Project sudah di-push ke GitHub

## 🚀 Langkah Deployment

### 1. Push ke GitHub

```bash
# Initialize git (jika belum)
git init
git add .
git commit -m "Initial commit"

# Connect ke GitHub repository
git remote add origin https://github.com/username/repo-name.git
git branch -M main
git push -u origin main
```

### 2. Deploy di Railway

1. **Login ke Railway**
   - Buka https://railway.app
   - Login dengan GitHub

2. **Create New Project**
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Pilih repository kamu
   - Railway akan otomatis detect Python app

3. **Configure Environment Variables**

   Klik tab "Variables" dan tambahkan:

   ```
   FLASK_SECRET_KEY=your-secret-key-here
   FLASK_DEBUG=False
   FLASK_PORT=5000
   ```

   Generate secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Deploy**
   - Railway akan otomatis build dan deploy
   - Tunggu sampai status "Deployed" (biasanya 2-5 menit)

5. **Get Public URL**
   - Klik tab "Settings"
   - Scroll ke "Domains"
   - Klik "Generate Domain"
   - Copy URL: `https://your-app.railway.app`

## ✅ Verifikasi Deployment

1. Buka URL Railway kamu
2. Coba login dengan Instagram
3. Check followers functionality

## 🔧 Troubleshooting

### Build Failed

**Cek logs:**
- Klik tab "Deployments"
- Klik deployment terakhir
- Lihat "Build Logs"

**Common issues:**
- Python version mismatch → pastikan `runtime.txt` ada
- Dependencies error → cek `requirements.txt`
- Missing files → pastikan semua file ter-commit

### App Crash / Error 502

**Cek logs:**
- Klik tab "Deployments"
- Klik "View Logs"

**Common issues:**
- Port tidak match → Railway auto-assign PORT env var
- Database path issue → pastikan pakai relative path
- Environment variables missing → cek tab Variables

### Database Persistence

Railway menyediakan **persistent storage** jadi database tidak akan hilang.

**Backup database:**
- Database SQLite tersimpan di folder `instance/`
- Untuk backup manual, bisa download dari Railway CLI

### Session Files

Session Instagram (`session_*.json`) akan tersimpan persistent di Railway.

**Notes:**
- Jangan commit session files ke git (sudah ada di .gitignore)
- Session akan tetap ada setelah redeploy
- Generate session sekali, pakai terus

## 🔄 Update Aplikasi

Setiap kali push ke GitHub, Railway otomatis redeploy:

```bash
git add .
git commit -m "Update feature X"
git push
```

Railway akan:
1. Auto-detect changes
2. Build ulang
3. Deploy versi baru
4. Zero downtime (old version tetap jalan sampai new version siap)

## 💰 Pricing

**Free Plan:**
- $5 credit per bulan
- Cukup untuk hobby project
- Auto-sleep jika tidak digunakan (tapi data tetap aman)

**Hobby Plan ($5/bulan):**
- $5 credit + $5 usage
- Tidak auto-sleep
- Lebih stabil untuk production

## 🎯 Railway CLI (Optional)

Install Railway CLI untuk manage dari terminal:

```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands
railway run python get_session.py

# Download database backup
railway run cat instance/unfollower_tracker.db > backup.db
```

## 📊 Monitoring

**Railway Dashboard:**
- CPU usage
- Memory usage
- Network traffic
- Deployment history

**Tips:**
- Check logs jika ada error
- Monitor usage untuk avoid overcharge
- Setup notifications di Settings

## 🔒 Security Best Practices

1. **Environment Variables**
   - Jangan hardcode secrets di code
   - Pakai Railway Variables untuk semua config

2. **Secret Key**
   - Generate random secret key
   - Jangan pakai example key di production

3. **Debug Mode**
   - Set `FLASK_DEBUG=False` di production
   - Debug info bisa expose sensitive data

4. **Session Files**
   - Jangan commit ke git
   - Railway storage sudah aman

## 🆘 Need Help?

**Railway Support:**
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app
- Community: https://help.railway.app

**Project Issues:**
- GitHub Issues: https://github.com/yourusername/yourrepo/issues

## 📖 Alternative Deployment

Jika Railway tidak cocok, cek:
- [Render.com](https://render.com) - Free tier bagus
- [Fly.io](https://fly.io) - Free allowance generous
- [Heroku](https://heroku.com) - Classic PaaS (paid)

Panduan lengkap di [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Happy deploying! 🚀**

Need help? Open an issue atau contact support.
