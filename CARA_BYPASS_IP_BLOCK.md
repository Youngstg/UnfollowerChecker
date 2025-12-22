# 🔓 Cara Bypass IP Block Instagram

Jika kamu mendapat error **"IP terblokir"** atau **"blacklist"**, gunakan panduan ini.

## 🎯 2 Metode Login

### Metode 1: Login dengan Password (Langsung)
- **Pros**: Mudah, cepat
- **Cons**: Bisa kena IP block dari Instagram
- **Cocok untuk**: First time setup dari IP yang belum pernah di-block

### Metode 2: Import Session JSON (Recommended!)
- **Pros**: Aman, tidak kena block, bisa digunakan berkali-kali
- **Cons**: Butuh sedikit setup awal
- **Cocok untuk**: Jika IP kamu sudah di-block atau untuk penggunaan jangka panjang

---

## 🚀 Cara 1: Login dari Komputer/IP Lain (Paling Mudah)

Jika IP rumah/kantor kamu di-block, login dari tempat lain:

### Opsi A: Hotspot dari HP
```
1. Disconnect WiFi
2. Nyalakan hotspot dari HP
3. Connect komputer ke hotspot HP
4. Login di web app
5. Session akan tersimpan
6. Selanjutnya bisa pakai WiFi normal lagi
```

### Opsi B: VPN
```
1. Install VPN (ProtonVPN, Windscribe, dll)
2. Connect ke server negara lain
3. Login di web app
4. Session akan tersimpan
5. Disconnect VPN untuk penggunaan normal
```

### Opsi C: Rumah Teman/Kafe
```
1. Bawa laptop ke rumah teman/kafe
2. Connect ke WiFi mereka
3. Login di web app
4. Session tersimpan di file
5. Copy file session_*.json ke komputer utama
```

---

## 🔧 Cara 2: Generate Session JSON (Recommended)

Generate session dari komputer/IP yang **tidak di-block**, lalu import ke web app.

### Step 1: Generate Session

Jalankan helper script:

```powershell
# Windows
python get_session.py

# Linux/Mac
python3 get_session.py
```

Script akan meminta:
- Username Instagram (tanpa @)
- Password

Lalu akan generate session JSON seperti ini:
```json
{
  "cookies": {
    ...
  },
  "uuids": {
    ...
  },
  ...
}
```

### Step 2: Copy Session JSON

Copy **SEMUA** output JSON (dari `{` sampai `}`)

### Step 3: Import ke Web App

1. Buka web app: http://localhost:5000
2. Klik tab **"Import Session"**
3. Masukkan username Instagram
4. Paste session JSON di textarea
5. Klik **"Import & Login"**

✅ Done! Sekarang kamu sudah login tanpa perlu password lagi.

---

## 🛡️ Cara 3: Manual Export Session File

Jika kamu punya akses ke komputer lain yang bisa login:

### Di Komputer yang Bisa Login:

1. Login ke web app
2. Session otomatis tersimpan di file `session_username.json`
3. Copy file ini

### Di Komputer Kamu:

1. Paste file `session_username.json` ke folder project
2. Login di web app dengan username yang sama
3. Web app akan otomatis pakai session file

---

## 💡 Cara 4: Tunggu IP Unblock (Pasif)

Instagram biasanya unblock IP setelah:
- **1-6 jam** untuk soft block
- **24 jam** untuk hard block

Selama menunggu:
1. Jangan coba login berulang kali (makin lama di-block)
2. Login manual di instagram.com untuk verify akun
3. Gunakan salah satu cara di atas

---

## 🔍 Troubleshooting

### "get_session.py juga kena block"

**Solusi:**
- Jalankan dari IP yang berbeda (hotspot HP, VPN, rumah teman)
- Atau gunakan cara manual:

```python
# Buat file manual_session.py
from instagrapi import Client
import json

cl = Client()

# GANTI INI
username = "username_kamu"
password = "password_kamu"

cl.login(username, password)
cl.dump_settings(f"session_{username}.json")

with open(f"session_{username}.json") as f:
    print(json.dumps(json.load(f), indent=2))
```

```bash
python manual_session.py
```

### "Session JSON tidak valid"

**Cek:**
- Copy lengkap dari `{` sampai `}`
- Tidak ada karakter tambahan di awal/akhir
- Format JSON valid (bisa cek di jsonlint.com)

### "Session expired"

Session Instagram expire setelah ~30 hari. Solusi:
- Generate session baru
- Atau login ulang dengan password

### "Masih kena block setelah import session"

Ini berarti akun Instagram kamu sendiri yang di-suspend. Solusi:
1. Buka instagram.com
2. Follow instruksi Instagram untuk verify akun
3. Tunggu 24 jam
4. Coba lagi

---

## 📖 Cara Kerja Session

Session = Cookie + Token yang Instagram berikan setelah login berhasil.

**Dengan session:**
- Tidak perlu password lagi
- Instagram sudah recognize device kamu
- Lebih aman karena tidak login berulang kali

**Session tersimpan di:**
- File: `session_username.json`
- Lokasi: Folder project

**Session valid selama:**
- ~30 hari (kalau tidak digunakan)
- Unlimited (kalau digunakan rutin)

---

## 🎓 Best Practices

1. **Generate session dari IP yang clean**
   - Jangan dari IP yang sering kena block
   - Gunakan hotspot HP atau VPN

2. **Simpan session file dengan aman**
   - Jangan share ke orang lain
   - Backup file session

3. **Gunakan session untuk penggunaan normal**
   - Login password hanya untuk generate session
   - Selanjutnya pakai session

4. **Jangan spam request**
   - Check followers max 1x per jam
   - Instagram limit rate per IP

5. **Refresh session berkala**
   - Generate session baru setiap 30 hari
   - Atau kalau session expired

---

## ✅ Checklist

Sudah coba semua ini?

- [ ] Restart router (dapat IP baru)
- [ ] Login dari hotspot HP
- [ ] Generate session dengan get_session.py
- [ ] Import session JSON di web app
- [ ] Copy session file dari komputer lain
- [ ] Login manual di instagram.com dulu
- [ ] Disable 2FA di Instagram
- [ ] Tunggu 24 jam untuk IP unblock

Kalau sudah semua tapi masih gagal, kemungkinan akun Instagram kamu yang bermasalah, bukan IP.

---

## 🆘 Masih Bermasalah?

1. Screenshot error message
2. Cek apakah bisa login di instagram.com (browser)
3. Cek apakah 2FA aktif
4. Cek log Instagram untuk "suspicious login attempts"

Jika masih stuck, bisa create issue dengan info:
- Error message
- Apakah bisa login di instagram.com
- Apakah 2FA aktif
- Sudah coba cara mana saja

---

**Selamat mencoba! 🚀**
