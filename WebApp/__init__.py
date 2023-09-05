from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin


db = SQLAlchemy()
admin = Admin()
DATABASE = "expence.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "@hello123"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
    db.init_app(app)
    admin.init_app(app)

    from .views import views
    from . authentication import authentication

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(authentication, url_prefix='/')

    from . models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "authentication.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists("/Web app" + DATABASE):
        with app.app_context():
            db.create_all()
        print("Created database")




   
