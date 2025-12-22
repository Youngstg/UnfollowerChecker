# ▲ Deployment ke Vercel

Panduan deploy Instagram Unfollower Checker ke Vercel.

## ⚠️ PENTING - Baca Dulu!

### Keterbatasan Vercel untuk Aplikasi Ini:

**❌ TIDAK RECOMMENDED** karena:

1. **Database Tidak Persistent**
   - Database di `/tmp` akan **HILANG** setiap kali function restart
   - Semua data followers history akan **RESET**
   - Session files akan **HILANG**

2. **Timeout 10 detik (Free) / 60 detik (Pro)**
   - Check followers bisa lebih dari 10 detik
   - Request akan **TIMEOUT** dan gagal

3. **Cold Start Problem**
   - Setiap request pertama sangat lambat (5-10 detik)
   - Instagram API connection bisa timeout

4. **Stateless Architecture**
   - Vercel serverless = stateless
   - Aplikasi ini butuh persistent storage
   - Session Instagram tidak bisa disimpan

### ✅ Lebih Baik Pakai:
- **Render.com** - Free tier dengan persistent storage
- **PythonAnywhere** - Always-on, persistent database
- **Fly.io** - Free tier bagus untuk Flask apps
- **Railway** - $5/bulan, paling mudah

---

## 📋 Jika Tetap Mau Coba Vercel

### Prerequisites

1. Akun GitHub
2. Akun Vercel (https://vercel.com)
3. Project sudah di-push ke GitHub

### Langkah Deployment

#### 1. Push ke GitHub

```bash
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

#### 2. Connect ke Vercel

1. Login ke https://vercel.com
2. Klik **"Add New Project"**
3. **Import Git Repository** → Pilih repo kamu
4. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./`
   - Build Command: (kosongkan)
   - Output Directory: (kosongkan)

#### 3. Set Environment Variables

Di Vercel dashboard, tambahkan:

```
FLASK_SECRET_KEY = your-secret-key-here
VERCEL = 1
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 4. Deploy

Klik **Deploy** dan tunggu ~2-5 menit.

#### 5. Test

Buka URL Vercel:
```
https://your-project.vercel.app
```

---

## 🐛 Masalah yang Akan Kamu Hadapi

### 1. Database Reset Setiap Deploy
**Problem:** Data followers hilang setiap kali deploy/restart

**Kenapa:** Vercel serverless tidak punya persistent storage

**Solusi:** Pakai external database
```python
# Ganti SQLite dengan PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')  # dari Supabase/Neon
```

Tapi ini ribet dan butuh setup database external.

### 2. Timeout Saat Check Followers
**Problem:** Request timeout setelah 10 detik

**Kenapa:** Vercel Free timeout = 10 detik, check followers butuh 15-30 detik

**Solusi:**
- Upgrade ke Vercel Pro ($20/bulan) untuk 60 detik timeout
- Atau pindah ke platform lain

### 3. Session Instagram Hilang
**Problem:** Harus login ulang terus

**Kenapa:** Session file di `/tmp` hilang setiap restart

**Solusi:** Store session di external storage (S3, Redis, dll) - RIBET!

### 4. Cold Start Lambat
**Problem:** Request pertama sangat lambat (10-15 detik)

**Kenapa:** Serverless function harus boot dulu

**Solusi:** Tidak ada untuk free tier

---

## 💰 Vercel Pricing

**Free (Hobby):**
- Unlimited deploys
- 100 GB bandwidth/bulan
- ❌ Timeout 10 detik (TERLALU PENDEK)
- ❌ No persistent storage
- ❌ Serverless execution only

**Pro ($20/bulan):**
- Timeout 60 detik (lebih baik tapi masih bisa kurang)
- Masih **NO persistent storage**
- Masih ada cold start

---

## 🔄 Alternatif yang Lebih Baik

### Perbandingan Platform:

| Feature | **Vercel** | **Render** | **PythonAnywhere** | **Fly.io** |
|---------|-----------|-----------|-------------------|-----------|
| **Persistent DB** | ❌ | ✅ | ✅ | ✅ |
| **Timeout** | 10-60s | No limit | No limit | No limit |
| **Cold Start** | Yes | Yes (free) | No | No |
| **Session Storage** | ❌ | ✅ | ✅ | ✅ |
| **Price** | Free | Free | Free | Free |
| **Best For** | Static sites | Full-stack apps | Python apps | Containers |

### Rekomendasi:

1. **PythonAnywhere** - Paling cocok untuk app ini
   - Always-on
   - Persistent database
   - Easy setup
   - Gratis permanent

2. **Render.com** - Alternatif bagus
   - Auto-deploy GitHub
   - Persistent storage
   - Auto-sleep tapi data aman

3. **Fly.io** - Production-ready
   - No sleep
   - Full VM control
   - Sedikit lebih kompleks

---

## 🎯 Kesimpulan

**JANGAN pakai Vercel untuk aplikasi ini** karena:
- ❌ Database reset terus
- ❌ Timeout terlalu pendek
- ❌ Session hilang
- ❌ Arsitektur tidak cocok

**Pakai platform yang support persistent storage:**
- ✅ PythonAnywhere (recommended)
- ✅ Render.com
- ✅ Fly.io
- ✅ Railway ($5/bulan)

---

## 📖 Next Steps

Jika Vercel tidak work (yang kemungkinan besar), ikuti panduan:

1. **PythonAnywhere**: (coming soon)
2. **Render.com**: (coming soon)
3. **Fly.io**: (coming soon)
4. **Railway**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

**Mau lanjut deployment ke platform lain yang lebih cocok?**

Pilih:
- [PythonAnywhere Guide] - Always-on, persistent, gratis
- [Render.com Guide] - Auto-deploy, persistent, gratis
- [Fly.io Guide] - Production-ready, gratis
- [Railway Guide](RAILWAY_DEPLOYMENT.md) - Paling mudah, $5/bulan

