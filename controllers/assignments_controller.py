from flask import render_template, request, redirect, url_for, Blueprint
from models import db
from models.assignments import Assignment
from datetime import datetime
#from models.skill import Skill

assignment_bp = Blueprint('assignment_bp', __name__)

@assignment_bp.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        name = request.form['name']
        grade_worth = request.form['grade_worth']
        due_date_string = request.form['due_date']
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()

        # TODO skill
        #skill = Skill(name="java", level=5)

        new_assignment = Assignment(name=name, grade_worth=grade_worth, due_date=due_date)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect("/")

    return render_template("add_assignment.html")