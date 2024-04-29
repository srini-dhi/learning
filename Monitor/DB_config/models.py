from flask import current_app as app
from DB_config import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    regions = db.Column(db.ARRAY(db.String(255)), nullable=True)

    def __init__(self, company_name, email, password, regions):
        self.company_name = company_name
        self.email = email
        self.password = password
        self.regions = regions

    def __repr__(self):
        return '<User %r>' % self.email
