from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """привязка базы данных к приложению"""

    with app.app_context():
        db.init_app(app)
        db.create_all()
