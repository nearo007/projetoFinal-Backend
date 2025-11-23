from functools import wraps
from flask import session, redirect, url_for, flash
from models.admin import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso restrito! Faça login.', 'danger')
            return redirect(url_for('user_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('Acesso restrito! Faça login.', 'danger')
                return redirect(url_for('user_bp.login'))

            user = User.query.get(user_id)
            if user is None or user.role not in roles:
                return redirect(url_for('user_bp.index'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator