from flask import render_template, request, redirect, url_for, Blueprint, session
from extensions import db, bcrypt
from models import User, Student, Classroom, Assignment
import os
from dotenv import load_dotenv

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
        
        if role not in ['teacher', 'admin']:
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(name=name, email=email, password=password_hash)
            db.session.add(new_user)
            db.session.commit()
        
        else:
            verify_code = request.form['verify_code']
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

            if role == 'teacher' and verify_code == TEACHER_REGISTER_CODE:
                new_user = User(name=name, email=email, password=password_hash, role=role)
                
            elif role == 'admin' and verify_code == ADMIN_REGISTER_CODE:
                new_user = User(name=name, email=email, password=password_hash, role=role)
            
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role

            return redirect(url_for("user_bp.index"))
        
        else:
            return redirect(url_for("user_bp.login"))


    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_role', None)
    # TODO flash message
    return redirect(url_for("user_bp.index"))