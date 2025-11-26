import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Ключ сесії
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key-change-in-prod"

    # Підключення до бази даних SQLite
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(basedir, "app.db")
    )

    # Вимкнення попереджень SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
