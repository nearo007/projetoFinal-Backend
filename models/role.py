from . import db
from .associations import role_skills


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    # relação com a outra tabela de skills
    skills = db.relationship('Skill', secondary=role_skills, back_populates='roles')