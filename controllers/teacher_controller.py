from flask import render_template, request, redirect, url_for, Blueprint, flash, session, current_app, send_from_directory, abort
from extensions import db
from models import Student, Classroom, Assignment, User, StudentAssignment
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from utils.decorators import login_required, role_required
from utils.data_range import get_assignment_range
from utils.files import allowed_file, save_assignment_pdf

teacher_bp = Blueprint('teacher_bp', __name__)

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
    classroom = Classroom.query.get_or_404(classroom_id)
    return render_template('classroom/classroom_details.html', classroom=classroom)

# assignments
@teacher_bp.route('/manage_assignments/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def manage_assignments(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)

    if session['user_role'] == 'teacher':
        assignments = Assignment.query.filter_by(teacher_id=session['user_id'], classroom_id=classroom_id).all()

    else:
        assignments = Assignment.query.filter_by(classroom_id=classroom_id)

    classroom = Classroom.query.get(classroom_id)
    return render_template("assignment/manage_assignments.html", assignments=assignments, classroom=classroom)
    
@teacher_bp.route('/teacher_student_details/<int:student_id>', methods=['GET'])
def teacher_student_details(student_id):
    student = Student.query.get_or_404(student_id)
    
    teacher_id = session.get('user_id')
    
    student_assignments = [
        sa for sa in student.student_assignments
        if sa.assignment.teacher_id == teacher_id
    ]
    
    if student_assignments:
        total_grade = 0
        count = 0
        
        for sa in student_assignments:
            if sa.assignment.grade_worth is not None and sa.assignment.grade_worth > 0:
                grade = sa.grade if sa.grade is not None else 0
                grade_ratio = (grade / sa.assignment.grade_worth) * 10
                total_grade += grade_ratio
                count += 1
        
        if count > 0:
            final_avg = round(total_grade / count, 10)
        else:
            None
    else:
        final_avg = None
    
    return render_template("student/teacher_student_details.html", student=student, student_assignments=student_assignments, final_avg=final_avg)

@teacher_bp.route('/create_assignment/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def create_assignment(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    
    if request.method == 'POST':
        name = request.form['name']
        grade_worth = request.form['grade_worth']
        due_date_string = request.form['due_date']
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()
        teacher_id = request.form['teacher_id']
        
        file = request.files.get("file")
        saved_file = save_assignment_pdf(file)

        new_assignment = Assignment(name=name, grade_worth=grade_worth, due_date=due_date, file=saved_file, teacher_id=teacher_id, classroom_id=classroom_id)
        db.session.add(new_assignment)
        db.session.commit()
        
        for student in classroom.students:
            grade_entry = StudentAssignment(student_id=student.id, assignment_id=new_assignment.id, grade=0)
            db.session.add(grade_entry)
        
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_assignments", classroom_id=classroom_id))

    data_range = get_assignment_range()
    return render_template("assignment/create_assignment.html", classroom=classroom, data_range=data_range)

@teacher_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename, as_attachment=True)


@teacher_bp.route("/delete_assignment/<int:assignment_id>", methods=['GET'])
@login_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    if not assignment:
        return redirect(url_for("teacher_bp.manage_assignments"))
    
    classroom = assignment.classroom
    
    db.session.delete(assignment)
    db.session.commit()

    return redirect(url_for("teacher_bp.manage_assignments", classroom_id=classroom.id))

@teacher_bp.route("/update_assignment/<int:assignment_id>", methods=['GET', 'POST'])
@login_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    classroom = assignment.classroom

    if not assignment:
        return redirect(url_for("teacher_bp.manage_assignments"))

    if request.method == 'POST':
        assignment_name = request.form['name']
        assignment_grade_worth = request.form['grade_worth']
        
        student_assignments = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()
        for sa in student_assignments:
            if sa.assignment.id == assignment.id:
                if sa.grade > float(assignment_grade_worth):
                    flash("Algum estudante possuí uma nota que excede o limite inserido!", "danger")
                    return redirect(url_for("teacher_bp.update_assignment", assignment_id=assignment.id))
        
        assignment_due_date_string = request.form['due_date']
        assignment_due_date = datetime.strptime(assignment_due_date_string, '%Y-%m-%d').date()

        assignment.name = assignment_name
        assignment.grade_worth = assignment_grade_worth
        assignment.due_date = assignment_due_date

        db.session.commit()
        return redirect(url_for("teacher_bp.manage_assignments", classroom_id=classroom.id))
    
    assignment_due_date = assignment.due_date.strftime('%Y-%m-%d')
    data_range = get_assignment_range()
    return render_template("assignment/update_assignment.html", assignment=assignment, assignment_due_date=assignment_due_date, data_range=data_range)

@teacher_bp.route('/update_grades/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def update_grades(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    classroom = assignment.classroom

    if request.method == 'POST':
        student_assignments = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()

        for sa in student_assignments:
            field_name = f"grade_{sa.student.id}"
            grade_value = request.form.get(field_name)

            if grade_value is not None and grade_value.strip() != "":
                try:
                    sa.grade = float(grade_value)
                except ValueError:
                    flash(f"Nota inválida para {sa.student.name}.", "warning")
                    continue

        db.session.commit()
        return redirect(url_for('teacher_bp.update_grades', assignment_id=assignment.id))

    student_assignments = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()
    return render_template('assignment/update_grades.html', assignment=assignment, classroom=classroom, student_assignments=student_assignments)