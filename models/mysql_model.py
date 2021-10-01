from __future__ import print_function

import sys

from flask_sqlalchemy import SQLAlchemy

from app import app

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://pizzeria-owner:n&jPrqRZL3r3sV7K@localhost:3307/pizzeria"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Artefact@localhost:3306/pizzeria"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:uv343vuUY126VUvv543uvhg6fyYYGYG@localhost:3306/pizzeria"

db = SQLAlchemy(app)

from models.domain.pizza import Pizza
from models.domain.ingredient import Ingredient


def save_new_pizza(name, ingredients):
    ingredients_list = []
    calculated_price = 1.0  # standard price
    veg_flag = True  # check if not veg
    for ingredient in ingredients:
        calculated_price = calculated_price + ingredient["price"]
        if not ingredient["vegetarian"]:
            veg_flag = False

        ingredient_found = Ingredient.query.filter_by(name=ingredient["name"]).first()
        print(ingredient_found, sys.stderr)
        if ingredient_found:
            ingredients_list.append(ingredient_found)
        else:
            ingredients_list.append(
                Ingredient(name=ingredient["name"],
                           vegetarian=ingredient["vegetarian"],
                           price=ingredient["price"])
            )

    new_pizza = Pizza(name=name,
                      vegetarian=veg_flag,
                      price=calculated_price,
                      ingredients=ingredients_list)
    db.session.merge(new_pizza)
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


def get_ingredients(pizza_name):
    pizza = find_single_pizza(pizza_name)
    return pizza.ingredients


# show_ingredients("Margherita")
# delete_pizza("Margherita")
db.create_all()
