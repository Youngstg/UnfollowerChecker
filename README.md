# Instagram Unfollower Checker - Web Application

Aplikasi web untuk tracking unfollowers Instagram secara otomatis. Cukup login sekali, lalu aplikasi akan menampilkan siapa yang unfollow kamu dan siapa yang tidak follow balik.

## Fitur

- **Login Otomatis**: Login ke Instagram melalui web app
- **Tracking Unfollowers**: Deteksi siapa yang unfollow kamu
- **Tidak Follow Balik**: Lihat siapa yang kamu follow tapi tidak follow balik
- **Riwayat**: Simpan riwayat perubahan followers
- **Grafik Statistik**: Visualisasi perubahan followers dan following
- **Dashboard Real-time**: Interface yang user-friendly

## Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Cara Menggunakan

### 1. Login
- Buka browser dan akses `http://localhost:5000`
- Masukkan username dan password Instagram kamu
- Klik "Login & Cek Unfollowers"

### 2. Dashboard
Setelah login, kamu akan melihat dashboard dengan:
- **Statistik**: Jumlah followers, following, unfollowers, dan yang tidak follow balik
- **Grafik**: Visualisasi perubahan followers dari waktu ke waktu
- **Daftar Unfollowers**: Siapa saja yang unfollow kamu dan kapan
- **Tidak Follow Balik**: Daftar akun yang kamu follow tapi tidak follow balik

### 3. Cek Followers
- Klik tombol "Cek Followers Sekarang" untuk update data
- Aplikasi akan mengambil data terbaru dari Instagram
- Data akan otomatis tersimpan di database

### 4. Tracking Otomatis
- Setiap kali kamu cek, aplikasi akan membandingkan dengan data sebelumnya
- Unfollowers baru akan terdeteksi dan ditampilkan
- Riwayat perubahan tersimpan di database

## Struktur File

```
UnfollowerChecker/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── unfollower_tracker.db       # SQLite database (auto-created)
├── templates/
│   ├── index.html             # Login page
│   └── dashboard.html         # Dashboard page
├── static/
│   ├── css/
│   │   └── style.css         # Styles
│   └── js/
│       └── dashboard.js      # Dashboard JavaScript
└── session_*.json            # Instagram session files (auto-created)
```

## Database Schema

### User
- `id`: Primary key
- `instagram_username`: Username Instagram
- `created_at`: Waktu dibuat
- `last_check`: Waktu terakhir cek

### FollowerSnapshot
- `id`: Primary key
- `user_id`: Foreign key ke User
- `timestamp`: Waktu snapshot
- `followers_count`: Jumlah followers
- `following_count`: Jumlah following
- `followers_data`: JSON data followers
- `following_data`: JSON data following

### UnfollowerEvent
- `id`: Primary key
- `user_id`: Foreign key ke User
- `username`: Username yang unfollow/tidak follow balik
- `event_type`: Tipe event (unfollowed_you, not_following_back)
- `detected_at`: Waktu terdeteksi

## Keamanan

- Password tidak disimpan di database
- Session Instagram disimpan di file lokal (session_*.json)
- Gunakan hanya untuk keperluan personal
- Jangan share session file dengan orang lain

## Troubleshooting

### Login Gagal
- Pastikan username dan password benar
- Jika ada 2FA, disable terlebih dahulu atau gunakan app password
- Jika Instagram meminta challenge, login melalui app Instagram dulu

### Rate Limit
- Instagram membatasi jumlah request
- Jangan terlalu sering cek followers (max 1x per jam)
- Jika kena rate limit, tunggu beberapa jam

### Session Expired
- Jika session expired, logout dan login lagi
- File session akan otomatis di-refresh

## Perbedaan dengan Script Lama

### Script Lama (Unfollow.py)
- Manual upload JSON file
- Tidak ada tracking riwayat
- Tidak ada grafik
- Harus download data dari Instagram setiap kali

### Web App Baru (app.py)
- Otomatis ambil data dari Instagram
- Tracking riwayat perubahan
- Grafik statistik interaktif
- Dashboard yang user-friendly
- Login sekali, data tersimpan otomatis

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite dengan SQLAlchemy ORM
- **Instagram API**: instagrapi library
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js

## Catatan Penting

1. **Gunakan dengan bijak**: Jangan spam request ke Instagram
2. **Rate limiting**: Instagram membatasi jumlah request per jam
3. **Akun pribadi**: Hanya untuk tracking akun pribadi sendiri
4. **Backup**: File database dan session penting untuk di-backup
5. **Privacy**: Jangan share credentials atau session file

## Development

Untuk development mode:

```bash
# Set Flask environment
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

# Run with auto-reload
python app.py
```

## API Endpoints

- `GET /` - Login page
- `POST /login` - Login handler
- `GET /dashboard` - Dashboard page
- `GET /check_followers` - Check followers endpoint (AJAX)
- `GET /stats` - Get statistics for chart (AJAX)
- `GET /logout` - Logout and clear session

## License

Untuk penggunaan personal saja.

## Support

Jika ada masalah atau bug, silakan buat issue di repository ini.
