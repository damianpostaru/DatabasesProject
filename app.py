from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://pizzeria-owner:n&jPrqRZL3r3sV7K@pizzeria-db:3306/pizzeria"
db = SQLAlchemy(app)
