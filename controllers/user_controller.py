from flask import render_template, request, redirect, url_for, Blueprint
from extensions import db, bcrypt
from models import User, Student, Classroom, Assignment

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
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(name=name, email=email, password=password_hash)
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
            return redirect(url_for("user_bp.index"))
        
        else:
            return redirect(url_for("user_bp.login"))


    return render_template("login.html")