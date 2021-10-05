from datetime import datetime, timedelta

from flask_apscheduler import APScheduler
from apscheduler.triggers.date import DateTrigger

from app import db, app
from models.ingredient import Ingredient
from models.pizza import Pizza
from models.dessert import Dessert
from models.drink import Drink
from models.menu_item import MenuItem
from models.order import Order
from models.order_item import OrderItem
from models.driver import Driver

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

INTERVAL_TASK_ID = 'preparation-time-id'


def save_new_pizza(name, ingredients):
    ingredients_list = []
    calculated_price = 1.0
    veg_flag = True
    for ingredient in ingredients:
        calculated_price = calculated_price + ingredient["price"]
        if not ingredient["vegetarian"]:
            veg_flag = False
        ingredient_found = Ingredient.query.filter_by(name=ingredient["name"]).first()
        if ingredient_found:
            ingredients_list.append(ingredient_found)
        else:
            ingredients_list.append(
                Ingredient(name=ingredient["name"], vegetarian=ingredient["vegetarian"], price=ingredient["price"]))
    new_pizza = Pizza(name=name, vegetarian=veg_flag, price=calculated_price, ingredients=ingredients_list)
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


def get_all_drinks():
    return Drink.query.all()


def get_all_desserts():
    return Dessert.query.all()


def show_ingredients(name):
    pizza = find_single_pizza(name)
    if len(pizza.ingredients) == 0:
        print(":(")
    for ingredient in pizza.ingredients:
        print(ingredient)


def save_new_order(address, customer_name, customer_number, order_items):
    order_time = datetime.today()
    new_order_items = []
    status = "In Process"
    for item in order_items:
        new_order_items.append(OrderItem(menu_item=item['menu_item'], quantity=item['quantity']))
    new_order = Order(address=address,
                      customer_name=customer_name,
                      customer_number=customer_number,
                      order_time=order_time,
                      status=status,
                      order_items=new_order_items)
    db.session.add(new_order)
    db.session.commit()

    def change_status():
        # new_order.status = "Out For Delivery"
        change_order = find_order(new_order.id)
        change_order.status = "Out For Delivery"
        db.session.commit()
        print("Pls")

    scheduler.add_job(id='preparation-time-id', func=change_status,
                      trigger=DateTrigger(order_time + timedelta(minutes=1)))
    return new_order


def find_order(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404(description='There is no order with id {}'.format(order_id))
    return order


def cancel_order(order_id):
    order = find_order(order_id)
    current_time = datetime.now()
    if order.status == "Cancelled":
        raise Exception("Order already cancelled.")
    if order.status == "Delivered":
        raise Exception("Order already delivered.")
    if ((current_time - order.order_time).seconds / 60) > 5:
        raise Exception("5 minutes have passed")
    order.status = "Cancelled"
    db.session.commit()


# show_ingredients("Margherita")
# delete_pizza("Margherita")
db.create_all()
