from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL 


app = Flask(__name__)
bootstrap = Bootstrap(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'user'
app.config['MYSQL_DATABASE_DB'] = 'mydatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'secret'

mysql.init_app(app)

from models import *
from forms import *
from app import view