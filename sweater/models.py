from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


from sweater import db, app, login_manager
from datetime import *

class Teachers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    surename = db.Column(db.String(50), nullable = False)
    subject = db.Column(db.String(50), nullable = False)
    salary = db.Column(db.Integer, nullable = False, default = 200)
    age = db.Column(db.Integer, nullable = True)


class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    surename = db.Column(db.String(50), nullable = False)
    clas = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = True)


class Graduates(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    surename = db.Column(db.String(50), nullable = False)
    points = db.Column(db.Integer, nullable = True)


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    race_type = db.Column(db.String(50), nullable = False)
    position = db.Column(db.Integer, nullable = False)
    student_name = db.Column(db.String(50), nullable = False)
    student_surename = db.Column(db.String(50), nullable = True)


class Admins(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(50), nullable = False)


class News(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    header = db.Column(db.String(50), nullable = False)
    paragraph = db.Column(db.String(50), nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now())

@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))