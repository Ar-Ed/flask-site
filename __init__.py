from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from files.config import Config
import ipinfo

access_token = '123456789abc'
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
handler = ipinfo.getHandler(access_token)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from files.user.routes import users
    from files.posts.routes import posts
    from files.main.routes import main
    from files.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app