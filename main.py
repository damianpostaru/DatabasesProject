import flask
from flask import make_response, render_template, jsonify
from flask import request

from client.setup import setup
from models.mysql_model import *

setup()

@app.route('/test', methods=['GET', 'POST'])
def test():
    # GET request
    if request.method == 'GET':
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Success', 200


@app.route("/pizza/<name>")
def get_pizza(name):
    pizza = find_single_pizza(name)
    return render_template(
        'show_pizza.html',
        name=name,
        vegetarian=pizza.vegetarian,
        price=pizza.price)


@app.route("/drink/<name>")
def get_drink(name):
    drink = find_single_drink(name)
    return render_template(
        'show_drink.html',
        name=name,
        price=drink.price)


@app.route("/dessert/<name>")
def get_dessert(name):
    dessert = find_single_dessert(name)
    return render_template(
        'show_dessert.html',
        name=name,
        price=dessert.price)


@app.route("/pizza_id/<name>")
def get_pizza_id(name):
    pizza = find_single_pizza(name)

    if pizza is not None:
        return jsonify({"id": pizza.id})
    else:
        return make_response({"Error": f"Could not find {str(name)}"}, 404)


@app.route("/drink_id/<name>")
def get_drink_id(name):
    drink = find_single_drink(name)

    if drink is not None:
        return jsonify({"id": drink.id})
    else:
        return make_response({"Error": f"Could not find {str(name)}"}, 404)


@app.route("/dessert_id/<name>")
def get_dessert_id(name):
    dessert = find_single_dessert(name)
    if dessert is not None:
        return jsonify({"id": dessert.id})
    else:
        return make_response({"Error": f"Could not find {str(name)}"}, 404)


@app.route("/")
def get():
    return flask.redirect("/menu")


@app.route("/order/form")
def make_order():
    pizzas = get_all_pizzas()
    drinks = get_all_drinks()
    desserts = get_all_desserts()
    return render_template('order_form.html', pizzas=pizzas, drinks=drinks, desserts=desserts)


@app.route("/menu")
def get_menu():
    pizzas = get_all_pizzas()
    drinks = get_all_drinks()
    desserts = get_all_desserts()
    return render_template('show_menu.html', pizzas=pizzas, drinks=drinks, desserts=desserts)


@app.route("/create/driver", methods=["POST"])
def create_drive():
    data = request.json
    first_name = data["first_name"]
    last_name = data["last_name"]
    working_area = data["working_area"]

    try:
        save_new_driver(first_name, last_name, working_area)
    except Exception as e:
        return make_response({"error": f"could not add drive: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/menuItem/<name>")
def get_menu_item_name(name):
    x = "/menuItem/"
    pizza = find_single_pizza(name)
    drink = find_single_drink(name)
    dessert = find_single_dessert(name)
    if pizza is not None:
        x = f"{x}{pizza.id}/0/0"
    if drink is not None:
        x = f"{x}0/{drink.id}/0"
    if dessert is not None:
        x = f"{x}0/0/{dessert.id}"
    return flask.redirect(x)


@app.route("/menuItem/<pizza_id>/<drink_id>/<dessert_id>")
def get_menu_item_id(pizza_id, drink_id, dessert_id):
    if pizza_id == '0':
        pi = None
    else:
        pi = pizza_id
    if drink_id == '0':
        dr = None
    else:
        dr = drink_id
    if dessert_id == '0':
        de = None
    else:
        de = dessert_id

    item = MenuItem.query.filter_by(pizza_id=pi, drink_id=dr, dessert_id=de).first()

    return jsonify(id=item.id)


@app.route("/create/pizza", methods=["POST"])
def create_pizza():
    data = request.json
    name = data["name"]
    ingredients = data["ingredients"]

    try:
        save_new_pizza(name, ingredients)
    except Exception as e:
        return make_response({"error": f"could not add pizza: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/create/drink", methods=["POST"])
def create_drink():
    data = request.json
    name = data["name"]
    price = data["price"]

    try:
        save_new_drink(name, price)
    except Exception as e:
        return make_response({"error": f"could not add drink: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/create/dessert", methods=["POST"])
def create_dessert():
    data = request.json
    name = data["name"]
    price = data["price"]

    try:
        save_new_dessert(name, price)
    except Exception as e:
        return make_response({"error": f"could not add dessert: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/order", methods=["POST"])
def order():
    data = request.json
    customer = data["customer"]
    order_items = data["order_items"]

    try:
        save_new_order(customer, order_items)
    except Exception as e:
        return make_response({"error": f"could not order: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.route("/cancel", methods=["POST"])
def remove_pizza():
    data = request.json
    order_id = data["order_id"]
    try:
        cancel_order(order_id)
    except Exception as e:
        return make_response({"error": f"could not cancel order: {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # app.run()
