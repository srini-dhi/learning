from flask import Flask
# from DB_config import db
from DB_config.config import Config
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)