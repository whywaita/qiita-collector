from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'secret_key'

# set config
app.config.from_pyfile('config_file.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://' + \
    os.getenv('QC_MYSQL_USER', app.config['MYSQL_USER']) + \
    ':' + os.getenv('QC_MYSQL_PASS', app.config['MYSQL_PASS']) + \
    '@' + os.getenv('QC_MYSQL_SERVER', app.config['MYSQL_SERVER']) + \
    '/' + os.getenv('QC_MYSQL_DBNAME', app.config['MYSQL_DB_NAME'])
app.config['SQLALCHEMY_NATIVE_UNICODE'] = app.config['MYSQL_CHAR']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# instance init
db = SQLAlchemy(app)
db.init_app(app)

# redis
if os.getenv('QC_REDIS_URL') is not None:
    # if set QC_REDIS_URL, overwrite REDIS URL
    app.config['REDIS_URL'] = os.getenv('QC_REDIS_URL')
redis_store = FlaskRedis(app)
