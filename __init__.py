from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from colorama import init, Fore, Back, Style

db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MZvKzJmUl8gN6z5jptAO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024 # 5 gb max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CLOUD_FOLDER'] = 'cloud'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import Users
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

#logger
init()

