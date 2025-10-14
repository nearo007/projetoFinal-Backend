from . import db

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    __tablename__ = 'vacancies'