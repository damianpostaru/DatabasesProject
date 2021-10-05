from app import db
from models.pizza import Pizza
from models.ingredient import Ingredient
from models.dessert import Dessert
from models.drink import Drink
from models.menu_item import MenuItem
from models.order import Order
from models.order_item import OrderItem
from models.driver import Driver


def save_new_pizza(name, vegetarian, price, ingredients):
    ingredients_list = []
    for ingredient in ingredients:
        ingredient_found = Ingredient.query.filter_by(name=ingredient["name"]).first()
        if ingredient_found:
            ingredients_list.append(ingredient_found)
        else:
            ingredients_list.append(
                Ingredient(name=ingredient["name"], vegetarian=ingredient["vegetarian"], price=ingredient["price"]))
    new_pizza = Pizza(name=name, vegetarian=vegetarian, price=price, ingredients=ingredients_list)
    db.session.add(new_pizza)
    db.session.commit()
    new_menu_item = MenuItem(pizza_id=new_pizza.id, drink_id=None, dessert_id=None)
    db.session.add(new_menu_item)
    db.session.commit()
    return new_pizza


def save_new_drink(name, price):
    new_drink = Drink(name=name, price=price)
    db.session.add(new_drink)
    db.session.commit()
    new_menu_item = MenuItem(pizza_id=None, drink_id=new_drink.id, dessert_id=None)
    db.session.add(new_menu_item)
    db.session.commit()
    return new_drink


def save_new_dessert(name, price):
    new_dessert = Dessert(name=name, price=price)
    db.session.add(new_dessert)
    db.session.commit()
    new_menu_item = MenuItem(pizza_id=None, drink_id=None, dessert_id=new_dessert.id)
    db.session.add(new_menu_item)
    db.session.commit()
    return new_dessert


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


def save_new_order(order_items):
    new_order_items = []
    for item in order_items:
        new_order_items.append(OrderItem(menu_item=item['menu_item'], quantity=item['quantity']))
    new_order = Order(order_items=new_order_items)
    db.session.add(new_order)
    db.session.commit()
    return new_order


# show_ingredients("Margherita")
# delete_pizza("Margherita")
db.create_all()
