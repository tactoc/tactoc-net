from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import path, mkdir

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")

def create_app():
    try:
        if not path.exists(app.config['MEDIA_FOLDER']):
            mkdir(app.config['MEDIA_FOLDER'])
            print("Created /media")

        if not path.exists(app.config['TACTOCNET_FOLDER']):
            mkdir(app.config['TACTOCNET_FOLDER'])
            print("Created /media/tactoc-net")

        if not path.exists(app.config['UPLOADS_FOLDER']):
            mkdir(app.config['UPLOADS_FOLDER'])
            print("Created /media/tactoc-net/uploads")

        if not path.exists(app.config['CLOUD_FOLDER']):
            mkdir(app.config['CLOUD_FOLDER'])
            print("Created /media/tactoc-net/cloud")
    except Exception as e:
        print(e)
        

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

    return app



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, threaded=True)




