from database import db
from tables.users import User

def get_all_users():
    return db.session.query(User).all()

def get_user_by_id(id):
    return db.session.query(User).filter(User.id == id).first()