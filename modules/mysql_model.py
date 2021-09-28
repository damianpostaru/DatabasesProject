from flask_sqlalchemy import SQLAlchemy

from app import app

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://pizzeria-owner:n&jPrqRZL3r3sV7K@localhost:3307/pizzeria"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Artefact@localhost:3306/pizzeria"
db = SQLAlchemy(app)

from models.pizza import Pizza
from models.ingredient import Ingredient


def save_new_pizza(name, vegetarian, price, ingredients):
    ingredients_list = []
    for ingredient in ingredients:
        ingredients_list.append(
            Ingredient(name=ingredient["name"], vegetarian=ingredient["vegetarian"], price=ingredient["price"]))
    new_pizza = Pizza(name=name, vegetarian=vegetarian, price=price, ingredients=ingredients_list)
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


def show_ingredients(name):
    pizza = find_single_pizza(name)
    if len(pizza.ingredients) == 0:
        print(":(")
    for ingredient in pizza.ingredients:
        print(ingredient)


show_ingredients("Margherita")
# delete_pizza("Margherita")
db.create_all()
