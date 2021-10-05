import flask
from flask import make_response, render_template
from flask import request

from app import app
from models.mysql_model import *



@app.route("/test")
def get_test():
    return "Hello World"


@app.route("/pizza/<name>")
def get_pizza(name):
    pizza = find_single_pizza(name)
    return render_template('show_pizza.html', name=name, vegetarian=pizza.vegetarian, price=pizza.price)


@app.route("/")
def get():
    return flask.redirect("/menu")


@app.route("/menu")
def get_menu():
    pizzas = get_all_pizzas()
    drinks = get_all_drinks()
    desserts = get_all_desserts()
    return render_template('show_menu.html', pizzas=pizzas, drinks=drinks, desserts=desserts)


@app.route("/create/pizza", methods=["POST"])
def create_pizza():
    data = request.json
    name = data["name"]
    ingredients = data["ingredients"]

    try:
        save_new_pizza(name, ingredients)
    except Exception as e:
        return make_response({"error": f"could not add pizza {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/create/drink", methods=["POST"])
def create_drink():
    data = request.json
    name = data["name"]
    price = data["price"]

    try:
        save_new_drink(name, price)
    except Exception as e:
        return make_response({"error": f"could not add drink {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/create/dessert", methods=["POST"])
def create_dessert():
    data = request.json
    name = data["name"]
    price = data["price"]

    try:
        save_new_dessert(name, price)
    except Exception as e:
        return make_response({"error": f"could not add dessert {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/order", methods=["POST"])
def order():
    data = request.json
    address = data["address"]
    customer_name = data["customer_name"]
    customer_number = data["customer_number"]
    order_items = data["order_items"]

    try:
        save_new_order(address, customer_name, customer_number, order_items)
    except Exception as e:
        return make_response({"error": f"could not order {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/cancel", methods=["POST"])
def remove_pizza():
    data = request.json
    order_id = data["order_id"]
    try:
        cancel_order(order_id)
    except Exception as e:
        return make_response({"error": f"could not cancel order {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


if __name__ == "__main__":
    app.run(debug=True)
