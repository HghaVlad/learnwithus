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
                user = User.query.filter_by(login=login).first()
                if user:
                    if user.check_password(password):
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
                if res == 'no' or len(password) < 6 or len(User.query.filter_by(login=login).all()) == 1 \
                        or len(name) < 4 or len(surname) < 4:
                    return render_template("login_page.html", answer="Incorrect code or not all fields completed right"), 403
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
                if len(password) >= 6 and len(User.query.filter_by(login=login).all()) == 0 \
                        and len(name) >= 4 and len(surname) >= 4:
                    new_user = User()
                    new_user.reg_user(login, password, name, surname, grade)
                    session.clear()
                    session['login'] = new_user.login
                    session['user_id'] = new_user.id
                    return redirect("/home")
                elif len(password) < 6:
                    return render_template("reg_page.html", answer="Length of the pass should be more than 6")
                elif len(User.query.filter_by(login=login).all()) == 0:
                    return render_template("reg_page.html", answer="This login is already taken")
                elif len(name) < 4 or len(surname) < 4:
                    return render_template("reg_page.html", answer="Length of the name and second name should be more than 4")
            return render_template("reg_page.html", answer="Complete all fields. Be sure that size of login, name and second_name is more than 4. And the password's lenght is more than 6.  "), 403
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
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == 'Customer':
            return render_template("customer_home_page.html")
        elif user.role == "Executor":
            orders = ActiveOrder.query.filter_by(executor_id=user.executor_id()).all()
            return render_template("executor_home_page.html", orders=orders)
        elif user.role == "Admin":
            orders = ActiveOrder.query.filter_by().all()
            return render_template("executor_home_page.html", orders=orders)

    return render_template("404_exception.html")


# Список заявок исполнителя
@bl.route("/order_lists")
def order_lists():
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == "Executor":
            orders = PostedOrder.query.all()
            return render_template("see_order_lists.html", orders=orders)

    return render_template("404_exception.html")


# Принять заявку исполнителем
@bl.route("/accept_order", methods=["POST", "GET"])
def accept_order():
    order_id = request.args.get("order_id")
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == "Executor":
            if request.method == "POST":
                telegram_link = request.form.get("telegram_link")
                if telegram_link:
                    post_order = PostedOrder.query.filter_by(id=order_id).first()
                    new_order = ActiveOrder()
                    new_order.make_order(post_order, user.executor_id(), telegram_link)
                    db.session.delete(post_order)
                    db.session.commit()
                    return redirect("/order_lists")
            else:
                return render_template("accept_order.html")

    return render_template("404_exception.html")


# Завершить заявку исполнителем
@bl.route("/finish_order")  # Надо будет проработать механизм завершения
def finish_order():
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        order_id = request.args.get("order_id")
        if user.role == "Customer":
            order = ActiveOrder.query.filter_by(id=order_id).first()
            if order.customer.user_id == user.id:
                order.finish_order()
                db.session.delete(order)
                db.session.commit()
                return redirect("/home")
        elif user.role == "Executor":
            order = ActiveOrder.query.filter_by(id=order_id).first()
            if order.executor.user_id == user.id:
                order.finish_order()
                db.session.delete(order)
                db.session.commit()
                return redirect("/home")
        return render_template("404_exception.html")


# Создать заявку заказкиком
@bl.route("/add_order", methods=["POST", "GET"])
def customer_make_order():
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == "Customer":
            if request.method == "POST":
                subject = request.form.get("order_subject")
                description = request.form.get("order_description")
                if subject and description:
                    new_order = PostedOrder()
                    new_order.make_order(subject, description, user.customer_id())
                    return redirect("/home")
                else:
                    return render_template("add_order.html", answer="Enter all values")
            else:
                return render_template("add_order.html")

    return render_template("404_exception.html")


# Созданые заказчиком заявки
@bl.route("/my_orders", methods=["POST", "GET"])
def customer_orders():
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == "Customer":
            orders = PostedOrder.query.filter_by(customer_id=user.customer_id()).all()
            return render_template("my_orders.html", orders=orders)

    return render_template("404_exception.html")


# Отменить заявку заказчиком
@bl.route("/cancel_order", methods=["POST", "GET"])
def delete_order():
    order_id = request.args.get("order_id")
    order = PostedOrder.query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect("/my_orders")


# Просмотр активных заявок заказчиком
@bl.route("/active_orders")
def active_orders():
    if 'login' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user.role == "Customer":
            orders = ActiveOrder.query.filter_by(customer_id=user.customer_id()).all()
            return render_template("customer_active_orders.html", orders=orders)

    return render_template("404_exception.html")
