from flask import render_template, request, redirect, url_for, Blueprint, flash
from extensions import db
from models import Student, Classroom, Assignment
from datetime import datetime

teacher_bp = Blueprint('teacher_bp', __name__)

# student
@teacher_bp.route('/manage_students', methods=['GET'])
def manage_students():
    students = Student.query.all()
    classrooms = Classroom.query.all()
    
    for student in students:
        student.born_date = student.born_date.strftime("%d/%m/%Y")

    return render_template("student/manage_students.html", students=students, classrooms=classrooms)

@teacher_bp.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        name = request.form['name']
        born_date_string = request.form['born_date']
        born_date = datetime.strptime(born_date_string, '%Y-%m-%d').date()
        classroom_id = request.form['classroom_id']

        new_student = Student(name=name, born_date=born_date, classroom_id=classroom_id)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_students"))

    classrooms = Classroom.query.all()
    return render_template("student/create_student.html", classrooms=classrooms)
    
@teacher_bp.route('/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Aluno não encontrado.", "warning")
        return redirect(url_for("teacher_bp.manage_students"))
    
    db.session.delete(student)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("teacher_bp.manage_students"))

@teacher_bp.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get(student_id)
    
    if not student:
        flash("Algo deu errado.", "warning")
        return redirect(url_for("teacher_bp.manage_students"))
    
    if request.method == 'POST':
        student_name = request.form['name']
        student_born_date_string = request.form['born_date']
        student_born_date = datetime.strptime(student_born_date_string, '%Y-%m-%d').date()

        student.name = student_name
        student.born_date = student_born_date

        db.session.commit()
        flash("Aluno atualizado com sucesso!", "success")
        return redirect(url_for("teacher_bp.manage_students"))
        
    student_born_date = student.born_date.strftime("%Y-%m-%d")
    return render_template("student/update_student.html", student=student, student_born_date=student_born_date)

# classroom
@teacher_bp.route('/manage_classrooms', methods=['GET'])
def manage_classrooms():
    classrooms = Classroom.query.all()

    return render_template("classroom/manage_classrooms.html", classrooms=classrooms)

@teacher_bp.route('/create_classroom', methods=['GET', 'POST'])
def create_classroom():
    if request.method == 'POST':
        name = request.form['name']

        new_classroom = Classroom(name=name)
        db.session.add(new_classroom)
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_classrooms"))

    return render_template("classroom/create_classroom.html")

@teacher_bp.route("/delete_classroom/<int:classroom_id>", methods=['GET'])
def delete_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)

    if not classroom:
        flash("Turma não encontrada.", "warning")
        return redirect(url_for("teacher_bp.manage_classrooms"))
    
    db.session.delete(classroom)
    db.session.commit()
    
    flash("Aluno removido com sucesso!", "success")
    return redirect(url_for("teacher_bp.manage_classrooms"))

@teacher_bp.route('/update_classroom/<int:classroom_id>', methods=['GET', 'POST'])
def update_classroom(classroom_id):
    classroom = Classroom.query.get(classroom_id)
    
    if not classroom:
        flash("Algo deu errado.", "warning")
        return redirect(url_for("teacher_bp.manage_classrooms"))
    
    if request.method == 'POST':
        classroom_name = request.form['name']
        
        classroom.name = classroom_name

        db.session.commit()
        flash("Turma atualizada com sucesso!", "success")
        return redirect(url_for("teacher_bp.manage_classrooms"))
        
    return render_template("classroom/update_classroom.html", classroom=classroom)

# assignments
@teacher_bp.route('/manage_assignments', methods=['GET', 'POST'])
def manage_assignments():
    assignments = Assignment.query.all()

    for assignment in assignments:
        assignment.due_date = assignment.due_date.strftime("%d/%m/%Y")

    return render_template("assignment/manage_assignments.html", assignments=assignments)
    

@teacher_bp.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if request.method == 'POST':
        name = request.form['name']
        grade_worth = request.form['grade_worth']
        due_date_string = request.form['due_date']
        due_date = datetime.strptime(due_date_string, '%Y-%m-%d').date()

        new_assignment = Assignment(name=name, grade_worth=grade_worth, due_date=due_date)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect(url_for("teacher_bp.manage_assignments"))

    return render_template("assignment/create_assignment.html")

@teacher_bp.route("/delete_assignment/<int:assignment_id>", methods=['GET'])
def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)

    if not assignment_id:
        flash("Tarefa não encontrada.", "warning")
        return redirect(url_for("teacher_bp.manage_assignments"))
    
    db.session.delete(assignment)
    db.session.commit()

    return redirect(url_for("teacher_bp.manage_assignments"))

@teacher_bp.route("/update_assignment/<int:assignment_id>", methods=['GET', 'POST'])
def update_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)

    if not assignment:
        flash("Algo deu errado.", "warning")

    if request.method == 'POST':
        assignment_name = request.form['name']
        assignment_grade_worth = request.form['grade_worth']
        
        assignment_due_date_string = request.form['due_date']
        assignment_due_date = datetime.strptime(assignment_due_date_string, '%Y-%m-%d').date()

        assignment.name = assignment_name
        assignment.grade_worth = assignment_grade_worth
        assignment.due_date = assignment_due_date

        db.session.commit()
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("teacher_bp.manage_assignments"))
    
    assignment_due_date = assignment.due_date.strftime('%Y-%m-%d')   
    return render_template("assignment/update_assignment.html", assignment=assignment, assignment_due_date=assignment_due_date)
