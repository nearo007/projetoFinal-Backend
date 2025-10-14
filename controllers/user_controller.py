from flask import render_template, request, redirect, url_for, Blueprint
from models import db
from models.user import User
from models.skill import Skill

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def index():
    users = User.query.all()
    skills = Skill.query.all()
    
    return render_template("index.html", users=users, skills=skills)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")