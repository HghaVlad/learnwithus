from database import db
from active_orders import ActiveOrder

class PostedOrder(db.Model):
    """класс размещённых заказов"""

    __tablename__ = "posted_orders"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    # есть скрытое поле customer (Customer.id = customer_id)

    def __repr__(self):
        return f"Posted order {self.id}"

    def make_order(self, subject, description, customer_id):
        self.subject = subject
        self.description = description
        self.customer_id = customer_id
        db.session.add(self)
        db.session.commit()
