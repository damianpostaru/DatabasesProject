from flask_sqlalchemy import SQLAlchemy
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Artefact@localhost/pizzeria"
db = SQLAlchemy(app)


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Pizza {self.name}, vegetarian:{self.vegetarian}, with price {self.price}"


def save_new_pizza(name, vegetarian, price):
    new_pizza = Pizza(name=name, vegetarian=vegetarian, price=price)
    db.session.add(new_pizza)
    db.session.commit()
    return new_pizza


db.create_all()
