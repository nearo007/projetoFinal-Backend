from flask import render_template, request, redirect, url_for, Blueprint, flash
from extensions import db
from models import Student, Classroom, Assignment, User
from datetime import datetime
from utils.decorators import role_required

admin_bp = Blueprint('admin_bp', __name__)

# student
@admin_bp.route('/manage_students', methods=['GET'])
@role_required('admin')
def manage_students():
    students = Student.query.all()

    return render_template("student/manage_students.html", students=students)

@admin_bp.route('/create_student', methods=['GET', 'POST'])
@role_required('admin')
def create_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        born_date_string = request.form['born_date']
        born_date = datetime.strptime(born_date_string, '%Y-%m-%d').date()
        classroom_id = request.form['classroom_id']

        new_student = Student(name=name, email=email, born_date=born_date, classroom_id=classroom_id)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("admin_bp.manage_students"))

    classrooms = Classroom.query.all()
    return render_template("student/create_student.html", classrooms=classrooms)
    
@admin_bp.route('/delete_student/<int:student_id>', methods=['GET'])
@role_required('admin')
def delete_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Aluno não encontrado.", "warning")
        return redirect(url_for("admin_bp.manage_students"))
    
    db.session.delete(student)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("admin_bp.manage_students"))

@admin_bp.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Algo deu errado.", "warning")
        return redirect(url_for("admin_bp.manage_students"))
    
    if request.method == 'POST':
        student_name = request.form['name']
        student_born_date_string = request.form['born_date']
        student_born_date = datetime.strptime(student_born_date_string, '%Y-%m-%d').date()

        student.name = student_name
        student.born_date = student_born_date

        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
        return redirect(url_for("admin_bp.manage_students"))
        
    student_born_date = student.born_date.strftime("%Y-%m-%d")
    return render_template("student/update_student.html", student=student, student_born_date=student_born_date)

# classroom
@admin_bp.route('/manage_classrooms', methods=['GET'])
@role_required('admin')
def manage_classrooms():
    classrooms = Classroom.query.all()

    return render_template("classroom/manage_classrooms.html", classrooms=classrooms)

@admin_bp.route('/create_classroom', methods=['GET', 'POST'])
@role_required('admin')
def create_classroom():
    if request.method == 'POST':
        name = request.form['name']
        teacher_ids = request.form.getlist('teachers') # [0, 1, 2] (ids)

        new_classroom = Classroom(name=name)
        db.session.add(new_classroom)
        db.session.commit()
        
        for teacher_id in teacher_ids:
            teacher = User.query.get(teacher_id)
            new_classroom.teachers.append(teacher)
        
        db.session.commit()

        return redirect(url_for("admin_bp.manage_classrooms"))

    teachers = User.query.filter_by(role='teacher').all()
    return render_template("classroom/create_classroom.html", teachers=teachers)

@admin_bp.route("/delete_classroom/<int:classroom_id>", methods=['GET'])
@role_required('admin')
def delete_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)

    if not classroom:
        flash("Turma não encontrada.", "warning")
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    db.session.delete(classroom)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("admin_bp.manage_classrooms"))

@admin_bp.route('/update_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    
    if not classroom:
        flash("Algo deu errado.", "warning")
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    if request.method == 'POST':
        classroom_name = request.form['name']
        
        classroom.name = classroom_name

        db.session.commit()
        flash("Turma atualizada com sucesso!", "success")
        return redirect(url_for("admin_bp.manage_classrooms"))
        
    return render_template("classroom/update_classroom.html", classroom=classroom)