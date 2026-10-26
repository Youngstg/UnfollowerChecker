import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
    BadCredentials,
    PleaseWaitFewMinutes,
    ClientThrottledError,
    ProxyAddressIsBlocked
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
if os.getenv('VERCEL'):
    db_path = '/tmp/unfollower_tracker.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///unfollower_tracker.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram_username = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_check = db.Column(db.DateTime)
    snapshots = db.relationship('FollowerSnapshot', backref='user', lazy=True)

class FollowerSnapshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    followers_count = db.Column(db.Integer)
    following_count = db.Column(db.Integer)
    followers_data = db.Column(db.Text)  # JSON string
    following_data = db.Column(db.Text)  # JSON string

class UnfollowerEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(50))  # 'unfollowed_you', 'you_unfollowed', 'not_following_back'
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

def get_instagram_client(username=None):
    """
    Inisialisasi Instagram client dengan delay realistis,
    dukungan proxy (misal Cloudflare WARP / residential),
    dan persistensi device settings agar tidak dianggap bot.
    """
    cl = Client()
    cl.delay_range = [2, 5]

    # Dukungan proxy untuk VPS (misal: socks5://127.0.0.1:40000 dari Cloudflare WARP)
    proxy = os.getenv('INSTAGRAM_PROXY')
    if proxy and proxy.strip():
        cl.set_proxy(proxy.strip())

    # Jika username diberikan dan session file ada, muat pengaturannya
    if username:
        session_file = f"session_{username}.json"
        if os.path.exists(session_file):
            try:
                cl.load_settings(session_file)
            except Exception as e:
                app.logger.warning(f"Gagal memuat session file untuk {username}: {e}")

    return cl

def get_or_create_user(username):
    """Helper untuk mengambil atau mendaftarkan user di database lokal"""
    user = User.query.filter_by(instagram_username=username).first()
    if not user:
        user = User(instagram_username=username)
        db.session.add(user)
        db.session.commit()
    return user

@app.route('/')
def index():
    if 'instagram_username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    raw_username = request.form.get('username', '')
    username = raw_username.strip().replace('@', '').lower()
    password = request.form.get('password', '')
    session_json = request.form.get('session_json', '').strip()

    if not username:
        return render_template('index.html', error='Username Instagram tidak boleh kosong.')

    session_file = f"session_{username}.json"

    # Metode 1: Import Session JSON jika diisi
    if session_json:
        try:
            session_data = json.loads(session_json)
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f)

            cl = get_instagram_client(username)
            cl.load_settings(session_file)

            user_id = cl.user_id
            if not user_id:
                user_id = cl.user_id_from_username(username)

            session['instagram_username'] = username
            get_or_create_user(username)
            return redirect(url_for('dashboard'))
        except Exception as e:
            return render_template('index.html', error=f'Session JSON tidak valid: {str(e)}')

    # Metode 2: Login Langsung dengan Password
    if not password:
        return render_template('index.html', error='Password tidak boleh kosong.')

    cl = get_instagram_client(username)

    try:
        # Jika session file sudah ada dan masih aktif, gunakan kembali
        if os.path.exists(session_file):
            try:
                cl.load_settings(session_file)
                if cl.user_id:
                    session['instagram_username'] = username
                    get_or_create_user(username)
                    return redirect(url_for('dashboard'))
            except Exception:
                pass  # Lanjut login kredensial jika session kedaluwarsa

        # Lakukan login kredensial
        cl.login(username, password)
        cl.dump_settings(session_file)

        session['instagram_username'] = username
        get_or_create_user(username)
        return redirect(url_for('dashboard'))

    except TwoFactorRequired:
        # Simpan kredensial sementara di server session untuk diarahkan ke input kode 2FA
        session['pending_2fa'] = {
            'username': username,
            'password': password
        }
        return redirect(url_for('verify_2fa'))

    except ChallengeRequired:
        return render_template(
            'index.html',
            error='Instagram mendeteksi login baru dari server VPS dan meminta verifikasi keamanan (Challenge). '
                  'Solusi terbaik: Aktifkan 2FA (Aplikasi Autentikasi) di akun Instagram Anda agar kode dapat '
                  'dimasukkan langsung di web ini, atau gunakan tab "SESSIONID" untuk login instan via cookie browser.'
        )

    except BadCredentials:
        return render_template('index.html', error='Username atau password yang Anda masukkan salah.')

    except (PleaseWaitFewMinutes, ClientThrottledError):
        return render_template('index.html', error='Instagram membatasi permintaan ("Please wait a few minutes"). Tunggu beberapa menit sebelum mencoba kembali.')

    except ProxyAddressIsBlocked:
        return render_template('index.html', error='IP Server/VPS terblokir oleh Instagram. Silakan pasang Cloudflare WARP di VPS Anda atau atur INSTAGRAM_PROXY di .env.')

    except Exception as e:
        error_msg = str(e)
        if 'blacklist' in error_msg.lower() or 'ip' in error_msg.lower():
            return render_template(
                'index.html',
                error='IP VPS terdeteksi oleh blacklist Instagram. '
                      'Gunakan tab "SESSIONID" untuk login instan dengan cookie browser, atau aktifkan Cloudflare WARP di VPS.'
            )
        return render_template('index.html', error=f'Login gagal: {error_msg}')

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """Halaman dan proses verifikasi Two-Factor Authentication (OTP / Authenticator)"""
    pending = session.get('pending_2fa')
    if not pending:
        return redirect(url_for('index'))

    username = pending['username']
    password = pending['password']

    if request.method == 'POST':
        code = request.form.get('code', '').strip().replace(' ', '')
        if not code:
            return render_template('verify_2fa.html', username=username, error='Kode verifikasi wajib diisi.')

        cl = get_instagram_client(username)
        session_file = f"session_{username}.json"

        try:
            cl.login(username, password, verification_code=code)
            cl.dump_settings(session_file)

            session.pop('pending_2fa', None)
            session['instagram_username'] = username
            get_or_create_user(username)
            return redirect(url_for('dashboard'))

        except Exception as e:
            return render_template(
                'verify_2fa.html',
                username=username,
                error=f'Verifikasi kode gagal: {str(e)}. Pastikan kode dari authenticator/SMS masih berlaku.'
            )

    return render_template('verify_2fa.html', username=username)

@app.route('/cancel-2fa')
def cancel_2fa():
    """Batalkan alur verifikasi 2FA dan kembali ke awal"""
    session.pop('pending_2fa', None)
    return redirect(url_for('index'))

@app.route('/login-cookie', methods=['POST'])
def login_cookie():
    """Metode login alternatif menggunakan Cookie SessionID tanpa perlu password"""
    sessionid = request.form.get('sessionid', '').strip()
    if not sessionid:
        return render_template('index.html', error='Cookie SessionID tidak boleh kosong.')

    cl = get_instagram_client()

    try:
        cl.login_by_sessionid(sessionid)
        username = cl.username
        if not username:
            return render_template('index.html', error='Tidak dapat membaca akun dari SessionID. Pastikan sessionid benar.')

        session_file = f"session_{username}.json"
        cl.dump_settings(session_file)

        session['instagram_username'] = username
        get_or_create_user(username)
        return redirect(url_for('dashboard'))

    except Exception as e:
        return render_template(
            'index.html',
            error=f'Login via SessionID gagal: {str(e)}. Pastikan cookie sessionid masih aktif di browser Anda.'
        )

@app.route('/dashboard')
def dashboard():
    if 'instagram_username' not in session:
        return redirect(url_for('index'))

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    if not user:
        session.clear()
        return redirect(url_for('index'))

    # Dapatkan snapshot terakhir
    latest_snapshot = FollowerSnapshot.query.filter_by(user_id=user.id).order_by(FollowerSnapshot.timestamp.desc()).first()

    # Dapatkan histori yang unfollow
    recent_unfollowers = UnfollowerEvent.query.filter_by(
        user_id=user.id,
        event_type='unfollowed_you'
    ).order_by(UnfollowerEvent.detected_at.desc()).limit(50).all()

    # Dapatkan yang tidak follow balik
    not_following_back = UnfollowerEvent.query.filter_by(
        user_id=user.id,
        event_type='not_following_back'
    ).order_by(UnfollowerEvent.detected_at.desc()).all()

    return render_template(
        'dashboard.html',
        username=username,
        user=user,
        latest_snapshot=latest_snapshot,
        recent_unfollowers=recent_unfollowers,
        not_following_back=not_following_back
    )

@app.route('/check_followers')
def check_followers():
    if 'instagram_username' not in session:
        return jsonify({'error': 'Belum login'}), 401

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    if not user:
        return jsonify({'error': 'Data pengguna tidak ditemukan'}), 404

    try:
        session_file = f"session_{username}.json"
        if not os.path.exists(session_file):
            return jsonify({'error': 'File session tidak ditemukan, silakan login ulang.'}), 401

        cl = get_instagram_client(username)
        user_id = cl.user_id

        if not user_id:
            try:
                user_id = cl.user_id_from_username(username)
            except Exception:
                return jsonify({'error': 'Session kedaluwarsa, silakan login ulang.'}), 401

        # Ambil followers dan following
        try:
            followers = cl.user_followers(user_id)
            following = cl.user_following(user_id)
        except Exception as api_error:
            error_msg = str(api_error)
            if 'login' in error_msg.lower() or 'challenge' in error_msg.lower() or 'checkpoint' in error_msg.lower():
                return jsonify({'error': 'Session kedaluwarsa oleh Instagram. Silakan login kembali.'}), 401
            return jsonify({'error': f'Instagram API error: {error_msg}'}), 500

        followers_list = [u.username for u in followers.values()]
        following_list = [u.username for u in following.values()]

        # Ambil snapshot sebelumnya
        previous_snapshot = FollowerSnapshot.query.filter_by(user_id=user.id).order_by(FollowerSnapshot.timestamp.desc()).first()

        # Deteksi siapa yang unfollow
        new_unfollowers = []
        if previous_snapshot and previous_snapshot.followers_data:
            try:
                previous_followers = json.loads(previous_snapshot.followers_data)
                new_unfollowers = [f for f in previous_followers if f not in followers_list]

                for unfollower in new_unfollowers:
                    event = UnfollowerEvent(
                        user_id=user.id,
                        username=unfollower,
                        event_type='unfollowed_you'
                    )
                    db.session.add(event)
            except Exception as e:
                app.logger.warning(f"Error membandingkan snapshot: {e}")

        # Deteksi yang tidak follow balik
        not_following_back = [f for f in following_list if f not in followers_list]

        UnfollowerEvent.query.filter_by(user_id=user.id, event_type='not_following_back').delete()
        for person in not_following_back:
            event = UnfollowerEvent(
                user_id=user.id,
                username=person,
                event_type='not_following_back'
            )
            db.session.add(event)

        # Simpan snapshot baru
        snapshot = FollowerSnapshot(
            user_id=user.id,
            followers_count=len(followers_list),
            following_count=len(following_list),
            followers_data=json.dumps(followers_list),
            following_data=json.dumps(following_list)
        )
        db.session.add(snapshot)

        user.last_check = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'success': True,
            'followers_count': len(followers_list),
            'following_count': len(following_list),
            'new_unfollowers': new_unfollowers,
            'not_following_back_count': len(not_following_back)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    """Keluar dari sesi web tanpa menghapus session file agar device ID tidak direset"""
    session.pop('instagram_username', None)
    session.pop('pending_2fa', None)
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    if 'instagram_username' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    snapshots = FollowerSnapshot.query.filter_by(user_id=user.id).order_by(FollowerSnapshot.timestamp.asc()).all()

    chart_data = {
        'timestamps': [s.timestamp.strftime('%Y-%m-%d %H:%M') for s in snapshots],
        'followers': [s.followers_count for s in snapshots],
        'following': [s.following_count for s in snapshots]
    }

    return jsonify(chart_data)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    app.run(debug=debug_mode, host=host, port=port)
