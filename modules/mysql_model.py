from app import db
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.dessert import Dessert
from models.drink import Drink
from models.order import Order
from models.order_content import order_content
from models.driver import Driver


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


def save_new_order(address, customer_name, customer_number, order_time, pizzas, desserts, drinks):
    new_order = Order(address, customer_name, customer_number, order_time, pizzas, desserts, drinks)
    db.session.add(new_order)
    db.session.commit()
    return new_order


# show_ingredients("Margherita")
# delete_pizza("Margherita")
db.create_all()
