from flask import render_template, request, redirect, url_for, Blueprint, flash, session
from extensions import db
from models import Student, Classroom, Assignment, User
from datetime import datetime
from utils.decorators import login_required, role_required
from utils.data_range import get_assignment_range

teacher_bp = Blueprint('teacher_bp', __name__)

# assignments
@teacher_bp.route('/manage_assignments/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def manage_assignments(classroom_id):
    if session['user_role'] == 'teacher':
        assignments = Assignment.query.filter_by(teacher_id=session['user_id'], classroom_id=classroom_id).all()

    else:
        assignments = Assignment.query.filter_by(classroom_id=classroom_id)

    classroom = Classroom.query.get(classroom_id)
    return render_template("assignment/manage_assignments.html", assignments=assignments, classroom=classroom)
    
@teacher_bp.route('/create_assignment/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def create_assignment(classroom_id):
    if request.method == 'POST':
        name = request.form['name']
        grade_worth = request.form['grade_worth']
        due_date_string = request.form['due_date']
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()
        teacher_id = request.form['teacher_id']

        new_assignment = Assignment(name=name, grade_worth=grade_worth, due_date=due_date, teacher_id=teacher_id, classroom_id=classroom_id)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_assignments", classroom_id=classroom_id))

    data_range = get_assignment_range()
    return render_template("assignment/create_assignment.html", classroom_id=classroom_id, data_range=data_range)

@teacher_bp.route("/delete_assignment/<int:assignment_id>", methods=['GET'])
@login_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)

    if not assignment_id:
        return redirect(url_for("teacher_bp.manage_assignments"))
    
    db.session.delete(assignment)
    db.session.commit()

    return redirect(url_for("teacher_bp.manage_assignments"))

@teacher_bp.route("/update_assignment/<int:assignment_id>", methods=['GET', 'POST'])
@login_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        return redirect(url_for("teacher_bp.manage_assignments"))

    if request.method == 'POST':
        assignment_name = request.form['name']
        assignment_grade_worth = request.form['grade_worth']
        
        assignment_due_date_string = request.form['due_date']
        assignment_due_date = datetime.strptime(assignment_due_date_string, '%Y-%m-%d').date()

        assignment.name = assignment_name
        assignment.grade_worth = assignment_grade_worth
        assignment.due_date = assignment_due_date

        db.session.commit()
        return redirect(url_for("teacher_bp.manage_assignments"))
    
    assignment_due_date = assignment.due_date.strftime('%Y-%m-%d')
    data_range = get_assignment_range()
    return render_template("assignment/update_assignment.html", assignment=assignment, assignment_due_date=assignment_due_date, data_range=data_range)

# teacher home
@teacher_bp.route('/teacher_home', methods=['GET'])
@login_required
def teacher_home():
    classrooms = Classroom.query.all()
    teacher = User.query.get(session['user_id'])
    teacher_classrooms = teacher.classrooms
    return render_template('teacher_home.html', classrooms=classrooms, teacher_classrooms=teacher_classrooms)

@teacher_bp.route('/classroom_details/<int:classroom_id>', methods=['GET'])
@login_required
def classroom_details(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    return render_template('classroom/classroom_details.html', classroom=classroom)