from flask import Flask
from config import Config

from controllers.user_controller import user_bp
from controllers.skill_controller import skill_bp
from controllers.role_controller import role_bp

import os
from models import db

# instanciando o Flask, definindo templates
app = Flask(__name__, template_folder=os.path.join('view', 'templates'))

# configurando o db
app.config.from_object(Config)

# definindo as rotas
app.register_blueprint(user_bp)
app.register_blueprint(skill_bp)
app.register_blueprint(role_bp)

# inicializa o SQLAlchemy com a aplicação Flask
db.init_app(app)

# cria todas as tabelas do banco no contexto da aplicação
with app.app_context():
    db.create_all()

# executa a aplicação caso rode o script diretamente
if __name__ == '__main__':
    app.run(debug=True)