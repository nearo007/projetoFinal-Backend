from flask import render_template, request, redirect, url_for, Blueprint
from models import db
from models.skill import Skill

skill_bp = Blueprint('skill_bp', __name__)

@skill_bp.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        name = request.form['name']
        level = request.form['level']

        new_skill = Skill(name=name, level=level)
        db.session.add(new_skill)
        db.session.commit()

        return redirect("/")

    return render_template("add_skill.html")