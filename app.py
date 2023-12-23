import requests

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.utils import secure_filename

from forms import (
    SigninForm,
    SignupForm,
    FileForm,
)
from models import User, File

import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from utils import generate_code

app = Flask(__name__)






scheduler = BackgroundScheduler()
scheduler.start()
app = Flask(__name__)
app.secret_key = "123"
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "postgresql+psycopg2://postgres:root@localhost:5432/3_23_sqlalchemy"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:root@localhost:5432/Hotwheels"


db = SQLAlchemy(app)
login_manager = LoginManager(app)
UPLOAD_PATH = os.path.join(app.root_path, "static", "files")


class UserLogin:
    def __init__(
        self,
        user_id: int | None = None,
        username: str | None = None,
        user: User | None = None,
    ):
        if user_id:
            self.user = db.session.execute(
                select(User).where(User.id == user_id)
            ).scalar_one()
        elif username:
            self.user = db.session.execute(
                select(User).where(User.username == username)
            ).scalar_one()
        elif user:
            self.user = user
        else:
            raise TypeError("user_id or username or user args are required")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user.id)

@login_manager.user_loader
def load_user(user_id):
    try:
        return UserLogin(user_id=user_id)
    except NoResultFound:
        return


def delete_file(file:File, app:Flask):
    with app.app_context():
        db.session.delete(file)
        db.session.commit()



@app.route("/", methods=['GET', 'POST'])
def index():
    time = datetime.now() + timedelta(seconds=10)
    scheduler.add_job(
        func=generate_code, trigger="date", run_date=time
    )
    return "Hello World"


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            pw_hash = generate_password_hash(form.password.data)
            u = User(username=form.username.data, password=pw_hash)
            db.session.add(u)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        else:
            return redirect(url_for("signin"))
    return render_template("signup.html", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        try:
            user = db.session.execute(
                select(User).where(User.username == form.username.data)
            ).scalar_one()
        except NoResultFound:
            flash("Не існує такого користувача")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(UserLogin(user=user))
                return redirect(url_for("index"))
            flash("Неправильна пара логін-пароль")
    return render_template("signin.html", form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        expire = form.expiring_choice.data
        link_code = generate_code()
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_PATH, filename))

        if expire == 'one_time':
            new_file = File(filename=filename, expire_at=None, one_time=True, link_code=link_code)
        else:
            expire_at = datetime.now() + timedelta(seconds=int(expire))
            new_file = File(filename=filename, expire_at=expire_at, one_time=False, link_code=link_code)
            scheduler.add_job(
                func=delete_file, trigger="date", run_date=expire_at, args=[new_file, app]
            )

        db.session.add(new_file)
        db.session.commit()
        flash(f'File has been sent! Your code: {link_code}')

    return render_template("upload.html", form=form)



@app.route('/download/<link_code>')
def download_file(link_code):
    try:
        file = db.session.execute(
            select(File).where(File.link_code == link_code)
        ).scalar_one()

        filename = file.filename
        if file.one_time:
            db.session.delete(file)
            db.session.commit()
        return send_from_directory(directory=UPLOAD_PATH, path=filename, as_attachment=True)

    except NoResultFound:
        flash("File not found.")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)