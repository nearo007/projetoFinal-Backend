from flask import render_template, request, redirect, url_for, Blueprint, flash
from extensions import db
from models import Student, Classroom, Assignment, User, StudentAssignment
from datetime import datetime
from utils.decorators import role_required
from utils.data_range import get_age_range
from email_validator import validate_email, EmailNotValidError

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin_home', methods=['GET'])
@role_required('admin')
def admin_home():
    return render_template('admin_home.html')

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
        
        try:
            validate_email(email)
        
        except EmailNotValidError:
            flash("O email inserido é inválido!", "danger")
            return redirect(url_for("admin_bp.create_student"))

        new_student = Student(name=name, email=email, born_date=born_date, classroom_id=classroom_id)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("admin_bp.manage_students"))

    classrooms = Classroom.query.all()
    age_range = get_age_range()
    return render_template("student/create_student.html", classrooms=classrooms, age_range=age_range)
    
@admin_bp.route('/delete_student/<int:student_id>', methods=['GET'])
@role_required('admin')
def delete_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        return redirect(url_for("admin_bp.manage_students"))
    
    db.session.delete(student)
    db.session.commit()
    
    return redirect(url_for("admin_bp.manage_students"))

@admin_bp.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        return redirect(url_for("admin_bp.manage_students"))
    
    if request.method == 'POST':
        student_name = request.form['name']
        student_email= request.form['email']
        student_born_date_string = request.form['born_date']
        student_born_date = datetime.strptime(student_born_date_string, '%Y-%m-%d').date()
        student_classroom_id = request.form['classroom_id']
        student_classroom = Classroom.query.get(student_classroom_id)
        
        try:
            validate_email(student_email)
        
        except EmailNotValidError:
            flash("O email inserido é inválido!", "danger")
            return redirect(url_for("admin_bp.update_student", student_id=student_id))

        student.name = student_name
        student.email = student_email
        student.born_date = student_born_date
        student.classroom = student_classroom

        db.session.commit()
        return redirect(url_for("admin_bp.manage_students"))
        
    student_born_date = student.born_date.strftime("%Y-%m-%d")
    classrooms = Classroom.query.all()
    age_range = get_age_range()
    return render_template("student/update_student.html", student=student, student_born_date=student_born_date, classrooms=classrooms, age_range=age_range)

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
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    db.session.delete(classroom)
    db.session.commit()
    
    return redirect(url_for("admin_bp.manage_classrooms"))

@admin_bp.route('/update_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    
    if not classroom:
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    if request.method == 'POST':
        classroom_name = request.form['name']
        teacher_ids = request.form.getlist('teachers') # [0, 1, 2] (ids)

        classroom.name = classroom_name
        
        classroom.teachers.clear()
        for teacher_id in teacher_ids:
            teacher = User.query.get(teacher_id)
            classroom.teachers.append(teacher)

        db.session.commit()
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    teachers = User.query.filter_by(role='teacher').all()
    return render_template("classroom/update_classroom.html", classroom=classroom, teachers=teachers)

@admin_bp.route('/read_grades/<int:assignment_id>', methods=['GET'])
@role_required('admin')
def read_grades(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    classroom = assignment.classroom

    student_assignments = StudentAssignment.query.filter_by(assignment_id=assignment.id).all()
    return render_template('assignment/read_grades.html', assignment=assignment, classroom=classroom, student_assignments=student_assignments)