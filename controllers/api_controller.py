from flask import Blueprint, jsonify, request
from models import Classroom, Assignment, Student, User
from extensions import db
from utils.decorators import login_required

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/classrooms', methods=['GET'])
@login_required
def api_get_classrooms():
    classrooms = Classroom.query.all()
    data = []
    
    for c in classrooms:        
        data.append({
            'id': c.id,
            'name': c.name,
            'students': len(c.students),
            'teachers': len(c.teachers)
            })
    
    return jsonify(data)

@api_bp.route('/students', methods=['GET'])
@login_required
def api_get_students():
    students = Student.query.all()
    data = []

    for s in students:
        data.append({
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'born_date': s.born_date.strftime('%Y-%m-%d'),
            'classroom_id': s.classroom_id
        })

    return jsonify(data)

@api_bp.route('/assignments', methods=['GET'])
@login_required
def api_get_assignments():
    assignments = Assignment.query.all()
    data = []

    for a in assignments:
        data.append({
            'id': a.id,
            'name': a.name,
            'grade_worth': a.grade_worth,
            'due_date': a.due_date.strftime('%Y-%m-%d') if a.due_date else None,
            'file': a.file,
            'teacher_id': a.teacher_id,
            'classroom_id': a.classroom_id
        })

    return jsonify(data)

@api_bp.route('/teachers', methods=['GET'])
@login_required
def api_get_teachers():
    teachers = User.query.filter_by(role='teacher').all()
    data = []

    for t in teachers:
        data.append({
            'id': t.id,
            'name': t.name,
            'email': t.email,
            'role': t.role,
            'classrooms': [
                {
                    'id': c.id,
                    'name': c.name
                }
                for c in t.classrooms
            ]
        })

    return jsonify(data)