from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import base64, uuid

from sweater.models import Teachers, Students, Admins, News, Graduates, Achievements
from sweater import db, app, login_manager


@app.route('/')
def main():
    # return render_template('tables.html')
    return redirect('/home')


# @app.route('/sign_up', methods = ['POST', 'GET'])
# def sign_up():
#     if request.method == 'POST':
#         admin = Admins(
#             name = request.form['name'],
#             password = generate_password_hash(request.form['password'], method='sha256')
#         )
#         try:
#             db.session.add(admin)
#             db.session.commit()
#         except Exception as error:
#             print(error)
#             return "Error"
#         return redirect('/')
#     else:
#         return render_template('sign-up.html')


@app.route('/home')
def home():
    news = News.query.all()
    news = news[len(news)-1]
    news_datetime = str(news.create_time)
    news_datetime = news_datetime[0:10],news_datetime[10:16]
    news_datetime = ''.join(news_datetime)
    return render_template('home.html', news=news, news_datetime=news_datetime)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        admin = Admins.query.filter_by(name = user_name).first()
        print(user_name)
        print(password)
        print(admin)
        if user_name and password and admin:
            if check_password_hash(admin.password, password):
                login_user(admin)
                return redirect('/tables')
            else:
                print('Şifrə Duzgun deyil !')
                return redirect('/')
        else:
            print('Məlumat daxil edilməyib !')
            return redirect('/sign_in')
    else:
        return render_template('sign-in.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/tables')
@login_required
def tables():
    students = Students.query.all()
    teachers = Teachers.query.all()
    news = News.query.all()
    graduates = Graduates.query.all()
    achievements = Achievements.query.all()
    return render_template('tables.html', students=students, teachers=teachers, newss=news, graduates=graduates, achievements=achievements)


@app.route('/teachers')
def teachers():
    teachers = Teachers.query.all()
    return render_template('teachers.html', teachers=teachers)


@app.route('/graduates')
def graduates():
    graduates = Graduates.query.all()
    return render_template('graduates.html', graduates=graduates)


@app.route('/achievements')
def achievements():
    achievements = Achievements.query.all()
    return render_template('achievements.html', achievements=achievements)


@app.route('/delete_news/<int:id>')
@login_required
def delete_news(id):
    object = News.query.filter_by(id = id).first()
    db.session.delete(object)
    db.session.commit()
    return redirect('/tables')


@app.route('/add_member/<string:type>', methods=['POST', 'GET'])
@login_required
def add_member(type):
    if type == 'teacher':
        if request.method == 'POST':
            teacher = Teachers(
                name = request.form['name'],
                surename = request.form['surename'],
                age  = request.form['age'],
                subject  = request.form['subject'],
                salary = request.form['salary']
            )
            try:
                db.session.add(teacher)
                db.session.commit()
            except Exception as error:
                print(error)
                return error
            return redirect('/tables')
        else:
            return render_template('add_member.html', type=type, list=['name', 'surename', 'age', 'subject', 'salary'])
    elif type == 'student':
        if request.method == 'POST':
            student = Students(
                name = request.form['name'],
                surename = request.form['surename'],
                clas = request.form['clas'],
                age = request.form['age']
            )
            try:
                db.session.add(student)
                db.session.commit()
            except Exception as error:
                print(error)
                return error
            return redirect('/tables')
        else:
            return render_template('add_member.html', type=type, list=['name', 'surename', 'clas', 'age'])
    elif type == 'graduate':
        if request.method == 'POST':
            graduate = Graduates(
                name = request.form['name'],
                surename = request.form['surename'],
                points = request.form['points']
            )
            try:
                db.session.add(graduate)
                db.session.commit()
            except Exception as error:
                print(error)
                return error
            return redirect('/tables')
        else:
            return render_template('add_member.html', type=type, list=['name', 'surename', 'points'])
    elif type == 'achievement':
        if request.method == 'POST':
            achievement = Achievements(
                race_type = request.form['race_type'],
                position = request.form['position'],
                student_name = request.form['student_name'],
                student_surename = request.form['student_surename']
            )
            try:
                db.session.add(achievement)
                db.session.commit()
            except Exception as error:
                print(error)
                return error
            return redirect('/tables')
        else:
            return render_template('add_member.html', type=type, list=['race_type', 'position', 'student_name', 'student_surename'])

@app.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news():
    if request.method == 'POST':
        news = News(
                header = request.form['header'],
                paragraph = request.form['paragraph'],
        )
        try:
            db.session.add(news)
            db.session.commit()
        except Exception as error:
            print(error)
            return error
        return redirect('/tables')
    else:
        return render_template('add_news.html')


@app.route('/edit/<string:type>/<int:id>', methods=['POST', 'GET'])
@login_required
def edit(id, type):
    if type == 'teacher':
        lst = ['name', 'surename', 'age', 'salary', 'delete']
    elif type == 'student':
        lst = ['name', 'surename', 'clas', 'age', 'delete']
    if request.method == 'POST':
        if type == 'teacher':
            Class = Teachers
            lst = ['name', 'surename', 'age', 'salary', 'delete']
            object = Class.query.get(id)
            name = request.form['name']
            surename = request.form['surename']
            age = request.form['age']
            salary = request.form['salary']
            sil = request.form['delete']
            if sil != 'sil':
                if id == int(object.id):
                    object.name = name
                    object.surename = surename
                    object.age = age
                    object.salary = salary
                    db.session.commit()
                return redirect('/tables')
            else:
                db.session.delete(object)
                db.session.commit()
                return redirect('/tables')
        elif type == 'student':
            Class = Students
            lst = ['name', 'surename', 'clas', 'age']
            object = Class.query.get(id)
            name = request.form['name']
            surename = request.form['surename']
            clas = request.form['clas']
            age = request.form['age']
            sil = request.form['delete']
            if sil != 'sil':
                if id == int(object.id):
                    object.name = name
                    object.surename = surename
                    object.clas = clas
                    object.age = age
                    db.session.commit()
                return redirect('/tables')
            else:
                db.session.delete(object)
                db.session.commit()
                return redirect('/tables')
    else:
        return render_template('edit.html', list = lst, type = type)


@app.route('/news', methods=['POST', 'GET'])
def news():
    news = News.query.all()
    return render_template('news.html', newss=news)

def db_init(app):
    with app.app_context():
        db.create_all()


db_init(app)

if __name__ == '__main__':
    app.run(debug=True)