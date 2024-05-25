from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import os
from forms import RegistrationForm, LoginForm, UploadForm
from models import db, user, post
from config import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'log in'

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.route('/')
@app.route('/home')
def home():
    posts = post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.vslidate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = user(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = form.picture.data
            picture_filename = picture_file.filename
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_filename)
            picture_file.save(picture_path)
            post = post(image_file=picture_filename, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your picture has been uploaded', 'success')
            return redirect(url_for('home'))
    return render_template('upload.html', title='upload', form=form)

if __name__ == '__main__':
    app.run(debug=True)
        


    
