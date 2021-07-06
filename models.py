from flask_login import UserMixin
from __init__ import db
# from sqlalchemy_utils import IPAddressType


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class SysAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    ip_address = db.Column(db.String(16))
    user_agent = db.Column(db.String(255))
    date_and_time = db.Column(db.DateTime)
