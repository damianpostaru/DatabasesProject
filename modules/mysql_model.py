from flask_sqlalchemy import SQLAlchemy

from app import app

# TODO: find how to set schema for mysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://pizzeria-owner:n&jPrqRZL3r3sV7K@localhost:5432/pizzeria-db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://pizzeria-owner:n&jPrqRZL3r3sV7K@localhost:3307/pizzeria"
db = SQLAlchemy(app)


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    __table_args__ = {'schema': 'pizzeria'}

    @staticmethod
    def deserialize(pizza_d: dict):
        return Pizza(**pizza_d)

    def __repr__(self):
        return f"Pizza {self.name}, vegetarian:{self.vegetarian}, with price {self.price}"


def save_new_pizza(name, vegetarian, price):
    new_pizza = Pizza(name=name, vegetarian=vegetarian, price=price)
    db.session.add(new_pizza)
    db.session.commit()
    return new_pizza


def find_single_pizza(name):
    pizza = Pizza.query.filter_by(name=name).first_or_404(description='There is no pizza with name {}'.format(name))
    return pizza


def delete_pizza(name):
    pizza = find_single_pizza(name)
    db.session.delete(pizza)
    db.session.commit()


def get_all_pizzas():
    return Pizza.query.all()


db.create_all()
