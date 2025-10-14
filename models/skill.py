from . import db
from .associations import role_skills

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=0)

    # relação invertida com a tabela de roles
    roles = db.relationship('Role', secondary=role_skills, back_populates='skills')