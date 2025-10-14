from . import db
#from .associations import role_skills

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade_worth = db.Column(db.Integer, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)

    # relação invertida com a tabela de roles
    #roles = db.relationship('Role', secondary=role_skills, back_populates='skills')