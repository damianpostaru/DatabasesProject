import flask
from flask import jsonify, make_response, render_template
from flask import request

from app import app
from modules.mysql_model import save_new_pizza, find_single_pizza, delete_pizza, get_all_pizzas, save_new_drink, \
    save_new_dessert


@app.route("/test/test")
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
    return render_template('show_menu.html', pizzas=pizzas)


@app.route("/create/pizza", methods=["POST"])
def create_pizza():
    data = request.json
    name = data["name"]
    vegetarian = data["vegetarian"]
    price = data["price"]
    ingredients = data["ingredients"]

    try:
        save_new_pizza(name, vegetarian, price, ingredients)
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


# @app.route("/order", methods=["POST"])
# def order():
#     data = request.json
#     pizzas = data["pizzas"]
#
#     try:
#         save_new_order(pizzas)
#     except Exception as e:
#         return make_response({"error": f"could not order {str(e)}"}, 400)
#     return make_response({"result": "success"}, 200)



@app.route("/delete/<name>", methods=["POST"])
def remove_pizza():
    data = request.json
    name = data["name"]
    try:
        delete_pizza(name)
    except Exception as e:
        return make_response({"error": f"could not delete pizza {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


@app.errorhandler(404)
def not_found():
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run(debug=True)
