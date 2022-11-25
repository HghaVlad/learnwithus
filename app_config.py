import os

basedir = os.path.abspath(os.path.dirname(__file__))
CODES_PATH = os.path.join(basedir, "codes.txt")

class Config(object):
    """настройка конфига flask приложения"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "LWU-top!"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
