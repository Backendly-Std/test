from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import base64, uuid
# from sweater import db, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = '@.'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = 'Zəhmət Olmaza Hesaba Daxil Olun'
login_manager.login_message_category = 'error'