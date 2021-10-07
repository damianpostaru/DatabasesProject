from app import db
from models.dessert import Dessert
from models.drink import Drink
from models.mysql_model import save_new_pizza, save_new_drink, save_new_dessert
from models.pizza import Pizza


def setup():
    emmentaler = {"name": "emmentaler", "vegetarian": True, "price": 1}
    mozzarella = {"name": "mozzarella", "vegetarian": True, "price": 1}
    gorgonzola = {"name": "gorgonzola", "vegetarian": True, "price": 1}
    goat_cheese = {"name": "goat_cheese", "vegetarian": True, "price": 1.50}

    if not db.session.query(Pizza).first():
        four_cheese = save_new_pizza("Four Cheese", [emmentaler, mozzarella, gorgonzola, goat_cheese])

    if not db.session.query(Drink).first():
        cola = save_new_drink("Cola", 1.99)
        sprite = save_new_drink("Sprite", 1.99)
        fanta = save_new_drink("Fanta", 1.99)
        beer = save_new_drink("Beer", 3.99)

    if not db.session.query(Dessert).first():
        chocolate_lavacake = save_new_dessert("Chocolate Lavacake", 2.99)
        chocolate_chip_cookie = save_new_dessert("Chocolate Chip Cookie", 1.99)
