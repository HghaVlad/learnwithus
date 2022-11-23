from flask import Blueprint, session, redirect, render_template, request
from database import db
from misc import check_code
from tables.users import User

bl = Blueprint("user_page", __name__)


@bl.route("/")
def start_page():
    if 'login' in session:
        return redirect("/home")
    else:
        return render_template("index.html")


# Авторизация пользователя
@bl.route("/login", methods=["POST", "GET"])
def login_page():
    if 'login' in session:
        return redirect("/home")
    else:
        if request.method == "POST":
            login = request.form.get("user_login")
            password = request.form.get("user_password")
            if login and password:
                user = User.query.filter_by(login=login)
                if user:
                    if user.first().check_password(password):
                        session.clear()
                        session['login'] = user.login
                        session['user_id'] = user.id
                        return redirect("/home")
            return render_template("login_page.html", answer="Incorrect password or login"), 403
        else:
            return render_template("login_page.html")


# Регистрация пользователя
@bl.route("/logup", methods=["POST", "GET"])
def reg_page():
    if 'login' in session:
        return redirect("/home")
    else:
        if request.method == "POST":
            login = request.form.get("user_login")
            password = request.form.get("user_password")
            name = request.form.get("user_name")
            surname = request.form.get("user_surname")
            grade = request.form.get("user_grade")
            code = request.form.get("user_code")
            if login and password and name and surname and grade and code:
                res = check_code(code)
                if res == 'no':
                    return render_template("login_page.html", answer="Incorrect code"), 403
                elif res == 'Admin':
                    new_user = User()
                    new_user.reg_admin(login, password)
                    session['login'] = new_user.login
                    session['user_id'] = new_user.id
                elif res == 'Executor':
                    new_user = User()
                    new_user.reg_executor(login, password, name, surname, grade)
                    session['login'] = new_user.login
                    session['user_id'] = new_user.id
                return redirect("/home")
            elif login and password and name and surname and grade:
                if len(password) > 6 and len(User.query.filter_by(login=login)) == 0 \
                        and len(name) > 4 and len(surname) > 4:
                    new_user = User()
                    new_user.reg_user(login, password, name, surname, grade)
                    session.clear()
                    session['login'] = new_user.login
                    session['user_id'] = new_user.id
                    return redirect("/home")

            return render_template("login_page.html", answer="Complete all fields"), 403
        else:
            return render_template("reg_page.html")


# Выход из сессии
@bl.route("/logout")
def log_out():
    session.clear()
    return redirect("/")


@bl.route("/home")
def home_page():
    if 'login' in session:
        pass
    else:
        return redirect('/')
