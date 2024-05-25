import os

class config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-gues'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'
    
