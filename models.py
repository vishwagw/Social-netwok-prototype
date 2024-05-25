from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 

db = SQLAlchemy()

class user(db.Model, UserMixin):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.string(20), unique=True, nullable=False)
    email = db.column(db.string(120), unique=True, nullable=False)
    password = db.column(db.string(60), nullable=False)
    posts = db.relationship('post', backref='author', lazy=True)

class post(db.model):
    id = db.column(db.Integer, primary_keys = True)
    image_files = db.column(db.string(20), nullable=False)
    date_posted = db.column(db.dateTime, nullable=False, default=datetime.utcnow)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
