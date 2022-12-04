from database import db
from tables.customers import Customer
from tables.executors import Executor
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """класс пользователя в бд"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String())
    role = db.Column(db.String())  # Роль пользователя(customer/executor/admin)

    customer_roles = db.relationship("Customer", backref="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.id}"

    def reg_user(self, login, password, name, surname, grade):
        self.login = login
        self.set_password(password)
        self.role = 'Customer'
        db.session.add(self)
        db.session.commit()
        new_customer = Customer()
        new_customer.new_customer(name, surname, grade, self.id)
        db.session.add(new_customer)
        db.session.commit()

    def reg_executor(self, login, password, name, surname, grade):
        self.login = login
        self.set_password(password)
        self.role = 'Executor'
        db.session.add(self)
        new_executor = Executor()
        new_executor.new_executor(name, surname, grade, self.id)
        db.session.add(new_executor)
        db.session.commit()

    def reg_admin(self, login, password):
        self.login = login
        self.set_password(password)
        self.role = 'Admin'
        db.session.add(self)
        db.session.commit()

    def executor_id(self):
        return Executor.query.filter_by(user_id=self.id).first().id

    def customer_id(self):
        return Customer.query.filter_by(user_id=self.id).first().id
