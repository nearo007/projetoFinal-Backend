from . import db

# tabela intermediaria para associação de roles e skills
role_skills = db.Table(
    'role_skills',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)