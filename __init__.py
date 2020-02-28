from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import path, mkdir
db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'MZvKzJmUl8gN6z5jptAO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024 # 10 gb max

app.config['MEDIA_FOLDER'] = '/media'
app.config['TACTOCNET_FOLDER'] = '/media/tactoc-net'
app.config['UPLOAD_FOLDER'] = '/media/tactoc-net/uploads'
app.config['CLOUD_FOLDER'] = '/media/tactoc-net/cloud'

try:
    if not path.exists(app.config['MEDIA_FOLDER']):
        mkdir(app.config['MEDIA_FOLDER'])
        print("Created /media")

    if not path.exists(app.config['TACTOCNET_FOLDER']):
        mkdir(app.config['TACTOCNET_FOLDER'])
        print("Created /media/tactoc-net")

    if not path.exists(app.config['UPLOAD_FOLDER']):
        mkdir(app.config['UPLOAD_FOLDER'])
        print("Created /media/tactoc-net/uploads")

    if not path.exists(app.config['CLOUD_FOLDER']):
        mkdir(app.config['CLOUD_FOLDER'])
        print("Created /media/tactoc-net/cloud")
except Exception as e:
    print(e)
    quit(0)

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



