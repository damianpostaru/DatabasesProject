from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://pizzeria-owner:n&jPrqRZL3r3sV7K@localhost:3307/pizzeria"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Artefact@localhost:3306/pizzeria"
db = SQLAlchemy(app)
