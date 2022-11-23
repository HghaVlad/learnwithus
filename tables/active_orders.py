from database import db


class ActiveOrder(db.Model):
    """класс принятых заказов"""

    __tablename__ = "active_orders"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    telegram_link = db.Column(db.String, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    # есть скрытое поле customer (Customer.id = customer_id)

    executor_id = db.Column(db.Integer, db.ForeignKey("executors.id"))
    # есть скрытое поле executor (Executor.id = executor_id)

    def __repr__(self):
        return f"History order {self.id}"
