from flask import render_template, request, redirect, url_for, Blueprint, flash
from extensions import db
from models import Student, Classroom, Assignment
from datetime import datetime

teacher_bp = Blueprint('teacher_bp', __name__)

# student
@teacher_bp.route('/manage_students', methods=['GET'])
def manage_students():
    students = Student.query.all()
    return render_template("student/manage_students.html", students=students)

@teacher_bp.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        name = request.form['name']
        born_date_string = request.form['born_date']
        born_date = datetime.strptime(born_date_string, '%Y-%m-%d').date()

        new_student = Student(name=name, born_date=born_date)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_students"))

    return render_template("student/create_student.html")
    
@teacher_bp.route('/remove_student/<int:student_id>', methods=['GET'])
def remove_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Aluno não encontrado.", "warning")
        return redirect(url_for("teacher_bp.manage_students"))
    
    db.session.delete(student)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("teacher_bp.manage_students"))

# classroom
@teacher_bp.route('/manage_classrooms', methods=['GET', 'POST'])
def manage_classrooms():
    pass

@teacher_bp.route('/create_classroom', methods=['GET', 'POST'])
def create_classroom():
    if request.method == 'POST':
        name = request.form['name']

        new_classroom = Classroom(name=name)
        db.session.add(new_classroom)
        db.session.commit()

        return redirect("/")

    return render_template("classroom/create_classroom.html")

# assignments
@teacher_bp.route('/manage_assignments', methods=['GET', 'POST'])
def manage_assignments():
    pass

@teacher_bp.route('/create_assignments', methods=['GET', 'POST'])
def create_assignments():
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

    return render_template("assignment/create_assignments.html")