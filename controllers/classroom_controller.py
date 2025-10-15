from flask import render_template, request, redirect, url_for, Blueprint
from models import db
from models.classroom import Classroom

classroom_bp = Blueprint('classroom_bp', __name__)

@classroom_bp.route('/manage_classrooms', methods=['GET', 'POST'])
def manage_classrooms():
    pass

@classroom_bp.route('/create_classroom', methods=['GET', 'POST'])
def create_classroom():
    if request.method == 'POST':
        name = request.form['name']

        new_classroom = Classroom(name=name)
        db.session.add(new_classroom)
        db.session.commit()

        return redirect("/")

    return render_template("classroom/create_classroom.html")