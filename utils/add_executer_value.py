from database import db
from tables.executors import Executor

def add_exec_val(val, user_id):
    executor = db.session.query(Executor).filter(Executor.user_id == user_id).first()
    executor.rating += val
    db.session.commit()
