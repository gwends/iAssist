from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.sign_in'
login.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app import models
    from app.users.routes import users
    from app.main.routes import main
    from app.jobs.routes import jobs

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(jobs)

    return app
