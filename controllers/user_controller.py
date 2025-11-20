from flask import render_template, request, redirect, url_for, Blueprint, session, flash, make_response
from extensions import db, bcrypt
from models import User, Student, Classroom, Assignment
import os, secrets
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
from utils.decorators import login_required

load_dotenv()

TEACHER_REGISTER_CODE = os.getenv('TEACHER_REGISTER_CODE')
ADMIN_REGISTER_CODE = os.getenv('ADMIN_REGISTER_CODE')

user_bp = Blueprint('user_bp', __name__)

@user_bp.before_app_request
def auto_login():
    if not session.get("logged_in"):
        token = request.cookies.get("remember_token")
        
        if token:
            user = User.query.filter_by(remember_token=token).first()
            if user:
                session['logged_in'] = True
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['user_email'] = user.email
                session['user_role'] = user.role

@user_bp.route('/')
def index():
    if session.get("logged_in"):
        if session.get("user_role") == "teacher":
            return redirect(url_for("teacher_bp.teacher_home"))
            
        else:
            return redirect(url_for("admin_bp.admin_home"))

    return render_template("index.html")

@user_bp.route('/webapp_functionality', methods=['GET'])
def webapp_functionality():
    return render_template("webapp_functionality.html")

@user_bp.route('/contact', methods=['GET'])
def contact():
    return render_template("contact.html")

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(name=name).first():
            flash("Esse usuário já existe no sistema!", "danger")
            return redirect(url_for("user_bp.register"))
        
        if User.query.filter_by(email=email).first():
            flash("Esse email já está cadastrado no sistema!", "danger")
            return redirect(url_for("user_bp.register"))
        
        try:
            validate_email(email)
        
        except EmailNotValidError:
            flash("O email inserido é inválido!", "danger")
            return redirect(url_for("user_bp.register"))
        
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            
        verify_code = request.form['verify_code']
        
        if not verify_code:
            flash("O código de verificação é obrigatório!", "danger")
            return redirect(url_for("user_bp.register"))
        
        elif role == 'teacher' and verify_code == TEACHER_REGISTER_CODE:
            new_user = User(name=name, email=email, password=password_hash, role=role)
            
        elif role == 'admin' and verify_code == ADMIN_REGISTER_CODE:
            new_user = User(name=name, email=email, password=password_hash, role=role)
        
        else:
            flash("O código de verificação está incorreto!", "danger")
            return redirect(url_for("user_bp.register"))
            
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for("user_bp.index"))
    
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        remember_password = request.form.get('remember_password')

        user = User.query.filter_by(name=name).first()
        
        if user:
            if not bcrypt.check_password_hash(user.password, password):
                flash("Senha incorreta!", "danger")
                return redirect(url_for("user_bp.login"))
        
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role
            
            response = make_response(redirect(url_for("user_bp.index")))

            if remember_password:
                token = secrets.token_urlsafe(64)
                user.remember_token = token
                db.session.commit()

                response.set_cookie(
                    'remember_token',
                    token,
                    max_age=60*60*24*30,
                    httponly=True,
                    secure=False
                )

            return response
            
        else:
            flash("Usuário não encontrado!", "danger")
            return redirect(url_for("user_bp.login"))
    
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            user.remember_token = None
            db.session.commit()

    session.clear()

    resp = make_response(redirect(url_for("user_bp.login")))
    resp.delete_cookie("remember_token")

    return resp


@user_bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        
        if user_name != session['user_name']:
            if User.query.filter_by(name=user_name).first():
                flash("Esse usuário já existe no sistema!", "danger")
                return redirect(url_for("user_bp.edit_user"))
        
        if user_email != session['user_email']:
            if User.query.filter_by(email=user_email).first():
                flash("Esse email já está cadastrado no sistema!", "danger")
                return redirect(url_for("user_bp.edit_user"))
        
        user = User.query.get(session['user_id'])
        
        user.name = user_name
        user.email = user_email
        
        db.session.commit()
        
        session['user_name'] = user.name
        session['user_email'] = user.email
        
        return redirect(url_for('user_bp.index'))
    
    return render_template("edit_user.html")

@user_bp.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        user = User.query.get(session['user_id'])
        
        if not bcrypt.check_password_hash(user.password, current_password):
                flash("A senha atual inserida é incorreta!", "danger")
                return redirect(url_for("user_bp.edit_password"))
        
        if new_password != confirm_password:
            flash("As senhas não coincidem!", "danger")
            return redirect(url_for("user_bp.edit_password"))
        
        password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = password_hash
        
        db.session.commit()
        return redirect(url_for("user_bp.logout"))
        
    
    return render_template("edit_password.html")