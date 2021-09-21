from flaskext.mysql import MySQL
import pymysql
from app import app

mysql = MySQL()
mysql.init_app(app)

