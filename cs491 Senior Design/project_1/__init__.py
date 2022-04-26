import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass1234@localhost/cs491'
    UPLOAD_FOLDER = 'project_1/static/images/'
    # C:\Users\Luis Garcia\OneDrive\Desktop\cs491 Senior Design\project_1\static\images
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    db.init_app(app)

    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Post, Tag, Comment, Rating, Downvote

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        return User.query.get(str(username))

    return app


