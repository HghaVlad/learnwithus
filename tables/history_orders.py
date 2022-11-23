from database import db


class HistoryOrder(db.Model):
    """класс прощлых заказов"""

    __tablename__ = "history_orders"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    # есть скрытое поле customer (Customer.id = customer_id)

    executor_id = db.Column(db.Integer, db.ForeignKey("executors.id"))
    # есть скрытое поле executor (Executor.id = executor_id)

    def __repr__(self):
        return f"History order {self.id}"
