from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    remember_token = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
    classrooms = db.relationship('Classroom', secondary='classroom_teachers', back_populates='teachers')

class Classroom(db.Model):
    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    students = db.relationship('Student', backref='classroom', lazy=True)
    
    teachers = db.relationship('User', secondary='classroom_teachers', back_populates='classrooms')

classroom_teachers = db.Table(
    'classroom_teachers',
    db.Column('classroom_id', db.Integer, db.ForeignKey('classrooms.id'), primary_key=True),
    db.Column('teacher_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    born_date = db.Column(db.DateTime, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)