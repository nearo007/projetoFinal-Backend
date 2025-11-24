from flask import render_template, request, redirect, url_for, Blueprint, flash
from extensions import db
from models import Student, Classroom, Assignment, User, StudentAssignment
from datetime import datetime
from utils.decorators import role_required
from utils.data_range import get_age_range
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin_home', methods=['GET'])
@role_required('admin')
def admin_home():
    return render_template('admin/admin_home.html')

@admin_bp.route('/manage_teachers', methods=['GET'])
@role_required('admin')
def manage_teachers():
    teachers = User.query.filter_by(role='teacher')
    
    return render_template("admin/manage_teachers.html", teachers=teachers)

@admin_bp.route('/delete_teacher/<int:teacher_id>', methods=['GET'])
@role_required('admin')
def delete_teacher(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    
    if not teacher:
        return redirect(url_for("admin_bp.manage_teachers"))
    
    db.session.delete(teacher)
    db.session.commit()
    
    return redirect(url_for("admin_bp.manage_teachers"))

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
        classroom_id = int(request.form['classroom_id'])
        
        try:
            validate_email(email)
        
        except EmailNotValidError:
            flash("O email inserido é inválido!", "danger")
            return redirect(url_for("admin_bp.create_student"))

        new_student = Student(name=name, email=email, born_date=born_date, classroom_id=classroom_id)
        db.session.add(new_student)
        db.session.commit()
        
        classroom = Classroom.query.get(classroom_id)
        
        for assignment in classroom.assignments:
            grade_entry = StudentAssignment(student_id=new_student.id, assignment_id=assignment.id, grade=0)
            db.session.add(grade_entry)
            
        db.session.commit()

        return redirect(url_for("admin_bp.manage_students"))

    classrooms = Classroom.query.all()
    age_range = get_age_range()
    return render_template("student/create_student.html", classrooms=classrooms, age_range=age_range)
    
@admin_bp.route('/delete_student/<int:student_id>', methods=['GET'])
@role_required('admin')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if not student:
        return redirect(url_for("admin_bp.manage_students"))
    
    for assignment in student.classroom.assignments:
        for sa in assignment.student_assignments:
            if sa.student.id == student.id:
                db.session.delete(sa)
    
    db.session.delete(student)
    db.session.commit()
    
    return redirect(url_for("admin_bp.manage_students"))

@admin_bp.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if not student:
        return redirect(url_for("admin_bp.manage_students"))
    
    old_classroom = student.classroom
    
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
        
        if old_classroom.id != student_classroom.id:
            for assignment in old_classroom.assignments:
                for sa in assignment.student_assignments:
                    if sa.student_id == student.id:
                        db.session.delete(sa)
    
            for assignment in student_classroom.assignments:
                new_sa = StudentAssignment(
                    student_id=student.id,
                    assignment_id=assignment.id,
                    grade=0
                )
                db.session.add(new_sa)

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

@admin_bp.route('/admin_student_details/<int:student_id>', methods=['GET'])
def admin_student_details(student_id):
    student = Student.query.get_or_404(student_id)

    assignments_by_teacher = {}
    for sa in student.student_assignments:
        teacher = sa.assignment.teacher
        if teacher not in assignments_by_teacher:
            assignments_by_teacher[teacher] = []
        assignments_by_teacher[teacher].append(sa)

    teacher_avgs = {}
    for teacher, assignments in assignments_by_teacher.items():
        total = 0
        count = 0

        for sa in assignments:
            if sa.assignment.grade_worth and sa.assignment.grade_worth > 0:
                grade = sa.grade if sa.grade is not None else 0
                ratio = (grade / sa.assignment.grade_worth) * 10
                total += ratio
                count += 1

        teacher_avgs[teacher] = round(total / count, 1) if count > 0 else None

    return render_template("student/admin_student_details.html", student=student, assignments_by_teacher=assignments_by_teacher, teacher_avgs=teacher_avgs)

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
    classroom = Classroom.query.get_or_404(classroom_id)

    if not classroom:
        return redirect(url_for("admin_bp.manage_classrooms"))
    
    try:
        for assignment in classroom.assignments:
            db.session.delete(assignment)

        if classroom.students:
            flash("Há estudantes atrelados a esta sala!", "danger")
            return redirect(url_for("admin_bp.manage_classrooms"))
        
        db.session.delete(classroom)
        db.session.commit()
    
    except IntegrityError:
        db.session.rollback()
        flash("Não foi possível excluir a sala.", "danger")
        
    return redirect(url_for("admin_bp.manage_classrooms"))

@admin_bp.route('/update_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_classroom(classroom_id):
    classroom = Classroom.query.get_or_404(classroom_id)
    
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