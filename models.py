# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from werkzeug.security import generate_password_hash, \
             check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    pwdhash = db.Column(db.String(1000000))  # TODO: 後で適切な値にする
    admin = db.Column(db.Boolean, default=0)

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    users_id = db.Column(
            db.Integer,
            db.ForeignKey('users.id')
            )

    user = sqlalchemy.orm.relationship(
            "User",
            backref=sqlalchemy.orm.backref(
                'favorites',
                order_by=id
                )
            )

    def __repr__(self):
        return '<Favorite %r>' % self.id
