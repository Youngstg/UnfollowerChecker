# Quick Start Guide

## Instalasi Cepat (Windows)

1. **Double click** `install.bat`
2. Tunggu hingga instalasi selesai
3. **Double click** `run.bat`
4. Buka browser: `http://localhost:5000`
5. Login dengan akun Instagram kamu

## Instalasi Manual

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jalankan aplikasi
python app.py

# 3. Buka browser
# http://localhost:5000
```

## Cara Pakai

### Pertama Kali

1. Buka `http://localhost:5000`
2. Masukkan username Instagram (tanpa @)
3. Masukkan password Instagram
4. Klik "Login & Cek Unfollowers"
5. Tunggu proses login (5-10 detik)

### Dashboard

Setelah login berhasil, kamu akan melihat:

- **Statistik** di bagian atas
  - Jumlah followers
  - Jumlah following
  - Total unfollowers yang terdeteksi
  - Jumlah yang tidak follow balik

- **Tombol "Cek Followers Sekarang"**
  - Klik untuk update data terbaru
  - Proses memakan waktu 10-30 detik tergantung jumlah followers
  - Jangan klik terlalu sering (max 1x per jam)

- **Grafik Followers**
  - Visualisasi perubahan followers dan following
  - Update otomatis setiap kali cek

- **Daftar Yang Unfollow Kamu**
  - Username dan waktu terdeteksi
  - Link ke profil Instagram
  - Bisa diklik untuk langsung ke profil

- **Daftar Yang Tidak Follow Balik**
  - Username yang kamu follow tapi tidak follow balik
  - Link ke profil Instagram

### Tips Penggunaan

1. **Cek Pertama Kali**: Data pertama adalah baseline, belum ada unfollowers
2. **Cek Berkala**: Cek 1x per hari atau per minggu untuk tracking
3. **Jangan Spam**: Instagram membatasi request, max 1x per jam
4. **Logout**: Klik "Logout" di kanan atas untuk keluar

## Troubleshooting

### "Login gagal"
- Cek username dan password
- Pastikan tidak ada typo
- Coba login di app Instagram dulu

### "2FA diperlukan"
- Disable 2FA di Instagram settings
- Atau gunakan app password

### "Challenge required"
- Login melalui app Instagram
- Selesaikan challenge/captcha
- Tunggu 1-2 jam lalu coba lagi

### "Session expired"
- Logout lalu login lagi
- File session akan di-refresh otomatis

### "Error loading data"
- Refresh halaman
- Logout dan login lagi
- Cek koneksi internet

## FAQ

**Q: Apakah aman?**
A: Ya, password tidak disimpan. Session disimpan lokal di komputer kamu.

**Q: Berapa lama proses cek?**
A: 10-30 detik tergantung jumlah followers/following.

**Q: Bisa auto cek setiap hari?**
A: Belum, tapi bisa ditambahkan fitur scheduler.

**Q: Data tersimpan dimana?**
A: Di file `unfollower_tracker.db` (SQLite database).

**Q: Bisa tracking multiple akun?**
A: Bisa, tapi harus logout dan login dengan akun lain.

**Q: Instagram ban akun gak?**
A: Kalau digunakan wajar (1x per hari), aman. Jangan spam request.

## Fitur Mendatang

- [ ] Auto check scheduler
- [ ] Export data ke CSV/Excel
- [ ] Notifikasi email/WhatsApp
- [ ] Multi-account support
- [ ] Analytics lebih detail
- [ ] Mobile responsive improvement

## Kontak

Jika ada masalah, silakan buat issue atau hubungi developer.
