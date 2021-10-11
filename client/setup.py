from app import db
from models.dessert import Dessert
from models.drink import Drink
from models.driver import Driver
from models.mysql_model import save_new_pizza, save_new_drink, save_new_dessert, save_new_driver
from models.pizza import Pizza


def setup():
    emmentaler = {"name": "emmentaler", "vegetarian": True, "price": 1}
    mozzarella = {"name": "mozzarella", "vegetarian": True, "price": 1}
    gorgonzola = {"name": "gorgonzola", "vegetarian": True, "price": 1}
    goat_cheese = {"name": "minced beef", "vegetarian": True, "price": 1.50}
    grilled_chicken = {"name": "grilled_chicken", "vegetarian": False, "price": 1}
    oregano = {"name": "oregano", "vegetarian": True, "price": 0}
    paprika = {"name": "paprika", "vegetarian": True, "price": 1}
    tomato = {"name": "tomato", "vegetarian": True, "price": 1}
    onion = {"name": "onion", "vegetarian": True, "price": 1}
    pepperoni = {"name": "pepperoni", "vegetarian": False, "price": 1}
    bacon = {"name": "bacon", "vegetarian": False, "price": 1}
    mushrooms = {"name": "mushrooms", "vegetarian": True, "price": 1}
    spinach = {"name": "spinach", "vegetarian": True, "price": 1}
    jalapenos = {"name": "jalapenos", "vegetarian": True, "price": 1}
    ham = {"name": "ham", "vegetarian": False, "price": 1}
    minced_beef = {"name": "minced_beef", "vegetarian": False, "price": 1}

    if not db.session.query(Pizza).first():
        four_cheese = save_new_pizza("Four Cheese", [emmentaler, mozzarella, gorgonzola, goat_cheese])
        chicken_supreme = save_new_pizza("Chicken Supreme", [grilled_chicken, mozzarella, oregano, paprika, onion, tomato])
        pepperoni_party = save_new_pizza("Pepperoni Party", [pepperoni, mozzarella])
        bbq_chicken_bacon = save_new_pizza("BBQ Chicken & Bacon", [bacon, grilled_chicken, mozzarella])
        veggi = save_new_pizza("Veggi", [mushrooms, mozzarella, paprika, onion, spinach, tomato])
        hot_spicy = save_new_pizza("Hot & Spicy", [jalapenos, mozzarella, paprika, pepperoni, onion])
        americana = save_new_pizza("Americana", [ham, mozzarella, pepperoni, minced_beef])
        creamy_bacon = save_new_pizza("Creamy Bacon", [bacon, mushrooms, ham, mozzarella, oregano, onion])
        margharita = save_new_pizza("Margharita", [mozzarella, oregano])
        bacon_onion = save_new_pizza("Bacon & Onion", [mozzarella, bacon, onion])

    if not db.session.query(Drink).first():
        cola = save_new_drink("Cola", 1.99)
        sprite = save_new_drink("Sprite", 1.99)
        fanta = save_new_drink("Fanta", 1.99)
        beer = save_new_drink("Beer", 3.99)

    if not db.session.query(Dessert).first():
        chocolate_lavacake = save_new_dessert("Chocolate Lavacake", 2.99)
        chocolate_chip_cookie = save_new_dessert("Chocolate Chip Cookie", 1.99)

    if not db.session.query(Driver).first():
        britt_de_jong = save_new_driver("Britt", "De Jong", "City center")
        bartholomeus_meyer = save_new_driver("Bartholomeus", "Meyer", "Wyck")
        elmo_bakker = save_new_driver("Elmo", "Bakker", "Stokstraat quarter")
        dwight_schrute = save_new_driver("Dwight", "Schrute", "Sphinx quarter")
        jim_halpert = save_new_driver("Jim", "Halpert", "Céramique")
        victor_htema = save_new_driver("Victor", "Htema", "Jeker quarter")
        francisca_van_dijk = save_new_driver("Francisca", "Van Dijk", "Sint Pieter")
