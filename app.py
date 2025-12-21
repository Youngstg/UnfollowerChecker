from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, TwoFactorRequired
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
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

def get_instagram_client():
    """Initialize Instagram client"""
    cl = Client()
    cl.delay_range = [1, 3]
    return cl

@app.route('/')
def index():
    if 'instagram_username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        cl = get_instagram_client()

        # Try to login
        cl.login(username, password)

        # Store session
        session['instagram_username'] = username

        # Get or create user in database
        user = User.query.filter_by(instagram_username=username).first()
        if not user:
            user = User(instagram_username=username)
            db.session.add(user)
            db.session.commit()

        # Save session file for future use
        session_file = f"session_{username}.json"
        cl.dump_settings(session_file)

        return redirect(url_for('dashboard'))

    except TwoFactorRequired:
        return render_template('index.html', error='2FA diperlukan. Silakan disable 2FA atau gunakan app password.')
    except ChallengeRequired:
        return render_template('index.html', error='Instagram memerlukan challenge. Silakan login melalui app Instagram terlebih dahulu.')
    except Exception as e:
        return render_template('index.html', error=f'Login gagal: {str(e)}')

@app.route('/dashboard')
def dashboard():
    if 'instagram_username' not in session:
        return redirect(url_for('index'))

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    # Get latest snapshot
    latest_snapshot = FollowerSnapshot.query.filter_by(user_id=user.id).order_by(FollowerSnapshot.timestamp.desc()).first()

    # Get recent unfollower events
    recent_unfollowers = UnfollowerEvent.query.filter_by(
        user_id=user.id,
        event_type='unfollowed_you'
    ).order_by(UnfollowerEvent.detected_at.desc()).limit(50).all()

    # Get not following back
    not_following_back = UnfollowerEvent.query.filter_by(
        user_id=user.id,
        event_type='not_following_back'
    ).order_by(UnfollowerEvent.detected_at.desc()).all()

    return render_template('dashboard.html',
                         username=username,
                         user=user,
                         latest_snapshot=latest_snapshot,
                         recent_unfollowers=recent_unfollowers,
                         not_following_back=not_following_back)

@app.route('/check_followers')
def check_followers():
    if 'instagram_username' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    try:
        cl = get_instagram_client()

        # Load session if exists
        session_file = f"session_{username}.json"
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(username, "")  # Login with session
        else:
            return jsonify({'error': 'Session expired, please login again'}), 401

        # Get user ID
        user_id = cl.user_id_from_username(username)

        # Get followers and following
        followers = cl.user_followers(user_id)
        following = cl.user_following(user_id)

        # Convert to lists of usernames
        followers_list = [user.username for user in followers.values()]
        following_list = [user.username for user in following.values()]

        # Get previous snapshot
        previous_snapshot = FollowerSnapshot.query.filter_by(user_id=user.id).order_by(FollowerSnapshot.timestamp.desc()).first()

        # Detect unfollowers
        new_unfollowers = []
        if previous_snapshot:
            previous_followers = json.loads(previous_snapshot.followers_data)
            new_unfollowers = [f for f in previous_followers if f not in followers_list]

            # Save unfollower events
            for unfollower in new_unfollowers:
                event = UnfollowerEvent(
                    user_id=user.id,
                    username=unfollower,
                    event_type='unfollowed_you'
                )
                db.session.add(event)

        # Detect not following back
        not_following_back = [f for f in following_list if f not in followers_list]

        # Clear old not_following_back events and add new ones
        UnfollowerEvent.query.filter_by(user_id=user.id, event_type='not_following_back').delete()
        for person in not_following_back:
            event = UnfollowerEvent(
                user_id=user.id,
                username=person,
                event_type='not_following_back'
            )
            db.session.add(event)

        # Create new snapshot
        snapshot = FollowerSnapshot(
            user_id=user.id,
            followers_count=len(followers_list),
            following_count=len(following_list),
            followers_data=json.dumps(followers_list),
            following_data=json.dumps(following_list)
        )
        db.session.add(snapshot)

        # Update user last check
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
    username = session.get('instagram_username')
    if username:
        # Remove session file
        session_file = f"session_{username}.json"
        if os.path.exists(session_file):
            os.remove(session_file)

    session.clear()
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    if 'instagram_username' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    username = session['instagram_username']
    user = User.query.filter_by(instagram_username=username).first()

    # Get all snapshots for chart
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
