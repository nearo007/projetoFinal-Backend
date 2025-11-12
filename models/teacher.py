from extensions import db

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade_worth = db.Column(db.Integer, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)

    teacher = db.relationship('User', backref='assignments')
    classroom = db.relationship('Classroom', backref='assignments')
    
    student_assignments = db.relationship('StudentAssignment', back_populates='assignment', cascade='all, delete-orphan', passive_deletes=True)
    
class StudentAssignment(db.Model):
    __tablename__ = 'student_assignments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    grade = db.Column(db.Float, nullable=True)

    student = db.relationship('Student', backref='student_assignments')
    assignment = db.relationship('Assignment', back_populates='student_assignments')