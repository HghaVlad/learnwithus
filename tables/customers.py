from database import db


class Customer(db.Model):
    """класс заказчиков"""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    grade = db.Column(db.String(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # есть скрытое поле user, которое хранит в себе ссылку на экземпляр класса User с id = user_id

    posted_orders = db.relationship("PostedOrder", backref="customer")
    history_orders = db.relationship("HistoryOrder", backref="customer")
    active_orders = db.relationship("ActiveOrder", backref="customer")

    def __repr__(self):
        return f"Customer {self.id}"
