from database import db
from tables.history_orders import HistoryOrder


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

    def make_order(self, posted_order, executor_id, telegram_link):
        self.subject = posted_order.subject
        self.description = posted_order.description
        self.telegram_link = telegram_link
        self.customer_id = posted_order.customer_id
        self.executor_id = executor_id
        db.session.add(self)
        db.session.commit()

    def finish_order(self):
        history_oder = HistoryOrder()
        history_oder.make(self)
        db.session.add(history_oder)
        db.session.commit()
        return history_oder.id
