from flask import Flask
from config import Config
from controllers.user_controller import user_bp
import os
from models import db

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)
app.register_blueprint(user_bp)

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)