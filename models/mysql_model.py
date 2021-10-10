from datetime import datetime, timedelta

from apscheduler.triggers.date import DateTrigger
from flask_apscheduler import APScheduler

from app import db, app
from models.address import Address
from models.customer import Customer
from models.dessert import Dessert
from models.drink import Drink
from models.driver import Driver
from models.ingredient import Ingredient
from models.menu_item import MenuItem
from models.order import Order
from models.order_item import OrderItem
from models.pizza import Pizza

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def save_new_pizza(name, ingredients):
    ingredients_list = []
    calculated_price = 0
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
    calculated_price = calculated_price + 0.4 * calculated_price  # 40% profit
    calculated_price = calculated_price + 0.09 * calculated_price  # 9% VAT
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
    pizza = Pizza.query.filter_by(name=name).first()
    return pizza


def find_single_drink(name):
    drink = Drink.query.filter_by(name=name).first()
    return drink


def find_single_dessert(name):
    dessert = Dessert.query.filter_by(name=name).first()
    return dessert


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


def save_new_order(customer, order_items):
    new_order_items = []
    customer_address = customer["address"]
    customer_area = customer_address["area"]
    customer_zip_code = customer_address["zip_code"]
    driver = get_first_available_driver(customer_area, customer_zip_code)
    driver_id = driver.id
    driver.available = False
    address = customer["address"]
    address_found = Address.query.filter_by(street=address["street"],
                                            house_number=address["house_number"],
                                            zip_code=address["zip_code"],
                                            area=address["area"]).first()
    if address_found:
        new_address = address_found
    else:
        new_address = Address(street=address["street"],
                              house_number=address["house_number"],
                              zip_code=address["zip_code"],
                              area=address["area"])
    db.session.add(new_address)
    db.session.commit()

    address_id = new_address.id
    customer_found = Customer.query.filter_by(first_name=customer["first_name"],
                                              last_name=customer["last_name"],
                                              phone_number=customer["phone_number"],
                                              address_id=address_id).first()
    if customer_found:
        new_customer = customer_found
    else:
        new_customer = Customer(first_name=customer["first_name"],
                                last_name=customer["last_name"],
                                phone_number=customer["phone_number"],
                                address_id=address_id)
    db.session.add(new_customer)
    db.session.commit()
    customer_id = new_customer.id
    for item in order_items:
        new_order_items.append(OrderItem(menu_item=item['menu_item'], quantity=item['quantity']))
    new_order = Order(customer_id=customer_id,
                      order_time=datetime.today(),
                      status="In Process",
                      driver_id=driver_id,
                      order_items=new_order_items)
    db.session.add(new_order)
    db.session.commit()
    order_id = new_order.id
    add_jobs_scheduler(order_id)

    return new_order


def add_jobs_scheduler(order_id):
    order_time = find_order(order_id).order_time

    def change_status():
        change_order = find_order(order_id)
        change_order.status = "Out For Delivery"
        print("Out For Delivery")
        db.session.commit()

    def deliver():
        change_order = find_order(order_id)
        change_order.status = "Delivered"
        print("Deliver")
        db.session.commit()

    def driver_back():
        change_order = find_order(order_id)
        busy_driver = find_driver(change_order.driver_id)
        busy_driver.available = True
        print("Driver Back")
        db.session.commit()

    # TODO: Change the times
    scheduler.add_job(id='preparation-time-'f'{order_id}', func=change_status,
                      trigger=DateTrigger(order_time + timedelta(minutes=0.1)))
    scheduler.add_job(id='delivery-time-'f'{order_id}', func=deliver,
                      trigger=DateTrigger(order_time + timedelta(minutes=0.2)))
    scheduler.add_job(id='driver-busy-time-'f'{order_id}', func=driver_back,
                      trigger=DateTrigger(order_time + timedelta(minutes=0.4)))


def save_new_driver(first_name, last_name, working_area):
    new_driver = Driver(first_name=first_name, last_name=last_name, working_area=working_area)
    db.session.add(new_driver)
    db.session.commit()
    return new_driver


def find_order(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404(description='There is no order with id {}'.format(order_id))
    return order


def find_address(address_id):
    address = Address.query.filter_by(id=address_id).first_or_404(
        description='There is no address with id {}'.format(address_id))
    return address


def find_driver(driver_id):
    driver = Driver.query.filter_by(id=driver_id) \
        .first_or_404(description='There is no driver with id {}'.format(driver_id))
    return driver

def find_customer(customer_id):
    customer = Customer.query.filter_by(id=customer_id) \
        .first_or_404(description='There is no driver with id {}'.format(customer_id))
    return customer


def cancel_order(order_id):
    order = find_order(order_id)
    current_time = datetime.now()
    if order.status == "Cancelled":
        raise Exception("Order already cancelled.")
    if order.status == "Delivered":
        raise Exception("Order already delivered.")
    if ((current_time - order.order_time).seconds / 60) > 5:
        raise Exception("5 minutes have passed")
    if scheduler.get_job('preparation-time-'f'{order_id}'):
        scheduler.remove_job('preparation-time-'f'{order_id}')
    if scheduler.get_job('delivery-time-'f'{order_id}'):
        scheduler.remove_job('delivery-time-'f'{order_id}')
    if scheduler.get_job('driver-busy-time-'f'{order_id}'):
        scheduler.remove_job('driver-busy-time-'f'{order_id}')
    order.status = "Cancelled"
    driver_id = order.driver_id
    driver = find_driver(driver_id)
    driver.available = True

    db.session.commit()


def are_there_available_drivers():
    drivers = db.session.query(Driver)
    for driver in drivers:
        if driver.available:
            return True
    return False


def get_first_available_driver(area, zip_code):
    if are_there_available_drivers():
        drivers = db.session.query(Driver)
        orders = db.session.query(Order)
        current_time = datetime.now()
        for driver in drivers:
            if driver.available and driver.working_area == area:
                return driver
            else:
                if driver.working_area == area:
                    for order in orders:
                        customer = find_customer(order.customer_id)
                        address = find_address(customer.address_id)
                        if address.area == area and ((current_time - order.order_time).seconds / 60) < 1 and address.zip_code == zip_code:
                            return driver

        raise Exception("There are no available drivers for your area.")
    else:
        raise Exception("There are no available drivers.")




db.create_all()
