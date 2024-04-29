from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Config():
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost:5432/test"
    SQLALCHEMY_TRACK_MODIFICATIONS = True