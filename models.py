# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """
    ユーザ
    """

    __tablename__ = "user"
    name = db.Column(db.UnicodeText, primary_key=True, nullable=False)

    def __init__(self, name):
        self.name = name
