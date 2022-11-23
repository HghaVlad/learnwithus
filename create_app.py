from flask import Flask


def create_app(config_obj):
    """создание экземляра flask приложения с нужным config'ом"""

    from tables.all_modules import Customer, Executor, User, PostedOrder, HistoryOrder

    app = Flask(__name__)
    app.config.from_object(config_obj)

    from database import init_db

    init_db(app)

    return app
