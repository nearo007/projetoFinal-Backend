from flask import render_template, request, redirect, url_for, Blueprint, flash
from models import db
from models.student import Student
from datetime import datetime
from controllers.user_controller import user_bp

student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/manage_students', methods=['GET'])
def manage_students():
    students = Student.query.all()
    return render_template("student/manage_students.html", students=students)

@student_bp.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        name = request.form['name']
        born_date_string = request.form['born_date']
        born_date = datetime.strptime(born_date_string, '%Y-%m-%d').date()

        new_student = Student(name=name, born_date=born_date)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("student_bp.manage_students"))

    return render_template("student/create_student.html")
    
@student_bp.route('/remove_student/<int:student_id>', methods=['GET'])
def remove_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Aluno não encontrado.", "warning")
        return redirect(url_for("student_bp.manage_students"))
    
    db.session.delete(student)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("student_bp.manage_students"))
