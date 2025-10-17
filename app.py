from flask import Flask
from config import Config
import os
from extensions import db, bcrypt
from controllers.user_controller import user_bp
from controllers.teacher_controller import teacher_bp


# instanciando o Flask, definindo templates
app = Flask(__name__, template_folder=os.path.join('view', 'templates'))

# configurando o db
app.config.from_object(Config)

# definindo as rotas
app.register_blueprint(user_bp)
app.register_blueprint(teacher_bp)

# inicializa o SQLAlchemy, e Bcrypt com a aplicação Flask
db.init_app(app)
bcrypt.init_app(app)

# cria todas as tabelas do banco no contexto da aplicação
with app.app_context():
    db.create_all()

# executa a aplicação caso rode o script diretamente
if __name__ == '__main__':
    app.run(debug=True)