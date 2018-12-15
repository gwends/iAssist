from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'users.sign_in'
login.login_message_category = 'info'


def page_not_found(e):
    return render_template('404.html'), 404


def internal_error(e):
    return render_template('500.html'), 500


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

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
