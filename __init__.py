from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# User database configuration
user_db = SQLAlchemy()
USER_DB_NAME = "users.db"

# We create a database to store the users


def create_app():
    app = Flask(__name__)

    # User database configuration
    app.config['SECRET_KEY'] = 'hjshj' # it's random
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{USER_DB_NAME}'
    

    
    # Initialize user and city databases
    user_db.init_app(app)

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(auth, url_prefix='/') # No particular prefix

    from website.models import User

    create_user_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_user_database(app):
    with app.app_context():
        if not path.exists('website/' + USER_DB_NAME):
            user_db.create_all()
            print('Created User Database!')
