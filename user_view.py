from flask import Blueprint, session, redirect, render_template, request
from database import db
from misc import check_code
from tables.users import User
from tables.active_orders import ActiveOrder
from tables.posted_orders import PostedOrder

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
                if res == 'no' or len(password) < 6 or len(User.query.filter_by(login=login)) == 1 \
                        or len(name) <= 4 or len(surname) <= 4:
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
        user = User.query.filter(id=session['user_id']).first()
        if user.role == 'Customer':
            return render_template("customer_home_page.html")
        elif user.role == "Executor":
            orders = ActiveOrder.query.filter(executor_id=user.id).all()
            return render_template("executor_home_page.html", orders=orders)
        elif user.role == "Admin":
            orders = ActiveOrder.query.filter().all()
            return render_template("executor_home_page.html", orders=orders)

    session.clear()
    return redirect("/")


# Список заявок исполнителя
@bl.route("/order_lists")
def order_lists():
    if 'login' in session:
        user = User.query.filter(id=session['user_id']).first()
        if user.role == "Executor":
            orders = PostedOrder.query.all()
            return render_template("see_order_lists.html", orders=orders)

    session.clear()
    return redirect("/")


# Принять заявку исполнителем
@bl.route("/accept_order")
def accept_order(order_id):
    if 'login' in session:
        user = User.query.filter(id=session['user_id']).first()
        if user.role == "Executor":
            if request.method == "POST":
                telegram_link = request.form.get("telegram_link")
                if telegram_link:
                    post_order = PostedOrder.query.filter(id=order_id)
                    new_order = ActiveOrder()
                    new_order.make_order(post_order, session['user_id'], telegram_link)
                    return redirect("/order_lists")
            else:
                return render_template("accept_order.html")

    session.clear()
    return redirect("/")


# Завершить заявку исполнителем
@bl.route("/finish_order")  # Надо будет проработать механизм завершения
def finish_order(order_id):
    order = ActiveOrder.query.filter(id=order_id)
    order.finish()
    db.session.delete(order)
    db.session.commit()
    return "Finished"


# Создать заявку закачкиком
@bl.route("/add_order")
def customer_make_order():
    if 'login' in session:
        user = User.query.filter(id=session['user_id']).first()
        if user.role == "Customer":
            if request.method == "POST":
                subject = request.form.get("order_subject")
                description = request.form.get("order_subject")
                if subject and description:
                    new_order = PostedOrder()
                    new_order.make_order(subject, description, user.id)
                    return redirect("/home")
                else:
                    return render_template("add_order.html", answer="Enter all values")
            else:
                return render_template("add_order.html")

    session.clear()
    return redirect("/")


# Созданые заказчиком заявки
@bl.route("/my_orders")
def customer_orders():
    if 'login' in session:
        user = User.query.filter(id=session['user_id']).first()
        if user.role == "Customer":
            orders = PostedOrder.query.filter(customer_id=user.id).all()
            return render_template("my_orders.html", orders=orders)

    session.clear()
    return redirect("/")


# Отменить заявку заказчиком
@bl.route("/cancel_order")
def delete_order(order_id):
    order = PostedOrder.query.filter(id=order_id).first()
    db.session.remove(order)
    db.session.commit()
    return "Finished"


# Просмотр активных заявок заказчиком
@bl.route("/active_orders")
def active_orders():
    if 'login' in session:
        user = User.query.filter(id=session['user_id']).first()
        if user.role == "Customer":
            orders = ActiveOrder.query.filter(customer_id=user.id).all()
            return render_template("customer_active_orders.html", orders=orders)

    session.clear()
    return redirect("/")
