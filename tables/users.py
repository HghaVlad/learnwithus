from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """класс пользователя в бд"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String())

    customer_roles = db.relationship("Customer", backref="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User {self.id}"
