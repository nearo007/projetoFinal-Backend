from flask import render_template, request, redirect, url_for, Blueprint, session, flash
from extensions import db, bcrypt
from models import User, Student, Classroom, Assignment
import os
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
from utils.decorators import login_required

load_dotenv()

TEACHER_REGISTER_CODE = os.getenv('TEACHER_REGISTER_CODE')
ADMIN_REGISTER_CODE = os.getenv('ADMIN_REGISTER_CODE')

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def index():
    users = User.query.all()
    students = Student.query.all()
    classrooms = Classroom.query.all()
    assignments = Assignment.query.all()

    return render_template("index.html", users=users, students=students, classrooms=classrooms, assignments=assignments)

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

            return redirect(url_for("user_bp.index"))
            
        else:
            flash("Usuário não encontrado!", "danger")
            return redirect(url_for("user_bp.login"))
    
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    session.pop('user_role', None)
    return redirect(url_for("user_bp.index"))

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