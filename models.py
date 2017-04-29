# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, \
             check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    pwdhash = db.Column(db.String(1000000))

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
