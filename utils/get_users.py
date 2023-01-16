from database import db
from tables.users import User
from tables.customers import Customer
from tables.executors import Executor


def get_all_users():
    users = db.session.query(User).all()
    for user in users:
        if user.role == "Customer" or user.role == "Admin":
            user_customer = Customer.query.filter_by(user_id=user.id).first()
            user.name = user_customer.name + " " + users.surname
            user.grade = user_customer.grade
        elif user.role == "Executor":
            user_executor = Executor.query.filter_by(user_id=user.id).first()
            user.name = user_executor.name + " " + users.surname
            user.grade = user_executor.grade
            user.rating = user_executor.rating
    return users


def get_user_by_id(id):
    return db.session.query(User).filter(User.id == id).first()