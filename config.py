import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"

    if os.environ.get("RENDER"):  # Render має цей env
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
