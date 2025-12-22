#!/usr/bin/env python3
"""
Helper script untuk mendapatkan Instagram session JSON
Gunakan ini jika IP kamu di-block oleh Instagram saat login langsung dari web app
"""

from instagrapi import Client
import json
import sys

def get_session():
    print("=" * 60)
    print("Instagram Session Generator")
    print("=" * 60)
    print()
    print("Script ini akan login ke Instagram dan generate session JSON")
    print("yang bisa kamu paste ke web app.")
    print()

    # Get credentials
    username = input("Instagram Username (tanpa @): ").strip()

    if not username:
        print("Error: Username tidak boleh kosong!")
        sys.exit(1)

    # Password dengan hidden input
    import getpass
    password = getpass.getpass("Instagram Password: ")

    if not password:
        print("Error: Password tidak boleh kosong!")
        sys.exit(1)

    print()
    print("Mencoba login ke Instagram...")
    print("(Ini mungkin memakan waktu 5-10 detik)")
    print()

    try:
        cl = Client()
        cl.delay_range = [1, 3]

        # Login
        cl.login(username, password)

        print("✅ Login berhasil!")
        print()

        # Save session
        session_file = f"session_{username}.json"
        cl.dump_settings(session_file)

        print(f"✅ Session saved to: {session_file}")
        print()

        # Read and print session
        with open(session_file, 'r') as f:
            session_data = json.load(f)

        print("=" * 60)
        print("SESSION JSON (Copy dan paste ke web app):")
        print("=" * 60)
        print()
        print(json.dumps(session_data, indent=2))
        print()
        print("=" * 60)
        print()
        print("📋 Cara menggunakan:")
        print("1. Copy semua text JSON di atas (dari { sampai })")
        print("2. Buka web app: http://localhost:5000")
        print("3. Klik tab 'Import Session'")
        print("4. Paste JSON di textarea")
        print("5. Klik 'Import & Login'")
        print()
        print(f"💾 Session juga sudah tersimpan di file: {session_file}")
        print("   Kamu bisa langsung login dengan username + password,")
        print("   session file akan otomatis digunakan.")
        print()

    except Exception as e:
        print(f"❌ Login gagal: {str(e)}")
        print()
        print("Kemungkinan penyebab:")
        print("- Username atau password salah")
        print("- 2FA aktif (disable dulu)")
        print("- Instagram memerlukan challenge")
        print("- IP address di-blacklist")
        print()
        print("💡 Solusi:")
        print("1. Pastikan username & password benar")
        print("2. Login manual di instagram.com dulu")
        print("3. Disable 2FA jika aktif")
        print("4. Coba dari komputer/IP yang berbeda")
        print("5. Atau gunakan VPN")
        sys.exit(1)

if __name__ == '__main__':
    get_session()
