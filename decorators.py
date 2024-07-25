from functools import wraps
from flask import session, redirect, url_for, flash
from datetime import datetime


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "info")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def spotify_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session or datetime.now().timestamp() > session.get('expires_at', 0):
            return redirect(url_for('get_spotify_info'))
        return f(*args, **kwargs)
    return decorated_function
