from flask import render_template, request, redirect, url_for, Blueprint
from models import db
from models.role import Role
from models.skill import Skill

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/add_role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        name = request.form['name']

        # TODO skill
        skill = Skill(name="java", level=5)

        new_role = Role(name=name, skills=[skill])
        db.session.add(new_role)
        db.session.commit()

        return redirect("/")

    return render_template("add_role.html")