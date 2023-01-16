from database import db


class Executor(db.Model):
    """класс исполнителей"""

    __tablename__ = "executors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    grade = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # есть скрытое поле user, которое хранит в себе ссылку на экземпляр класса User с id = user_id

    history_orders = db.relationship("HistoryOrder", backref="executor")
    active_orders = db.relationship("ActiveOrder", backref="executor")

    def __repr__(self):
        return f"Executor {self.id}"

    def new_executor(self, name, surname, grade, user_id):
        self.name = name
        self.surname = surname
        self.grade = grade
        self.user_id = user_id
