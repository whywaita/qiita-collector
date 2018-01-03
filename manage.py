# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import os

from sqlalchemy_utils import database_exists, create_database

from qc import app, db
from qc.models import User
import qc.routes

port = os.getenv('PORT', 5000)

# commands
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server("0.0.0.0", use_debugger=True, port=port))

# migrate (tmp)
db.init_app(app)
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()
if len(User.query.filter(User.name == 'admin').all()) == 0:
    admin = User('admin', 'password')
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
