from database import db
from tables.users import User
from tables.customers import Customer
from tables.executors import Executor


def get_all_users():
    users = db.session.query(User).all()
    for user in users:
        if user.role == "Customer":
            print(user)
            user_customer = Customer.query.filter_by(user_id=user.id).first()
            print(user_customer)
            user.name = user_customer.name + " " + user_customer.surname
            user.grade = user_customer.grade
        elif user.role == "Executor":
            print(user)
            user_executor = Executor.query.filter_by(user_id=user.id).first()
            print(user_executor)
            user.name = user_executor.name + " " + user_executor.surname
            user.grade = user_executor.grade
            user.rating = user_executor.rating

    return users


def get_user_by_id(id):
    return db.session.query(User).filter(User.id == id).first()