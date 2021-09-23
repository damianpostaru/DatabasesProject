from flask import jsonify, make_response, render_template
from flask import request

from app import app
from modules.mysql_model import save_new_pizza, Pizza, find_single_pizza, delete_pizza


@app.route("/test")
def get_test():
    return "Hello World"


@app.route("/pizza/<name>")
def get_pizza(name):
    pizza = find_single_pizza(name)
    return render_template('show_pizza.html', name=name, vegetarian=pizza.vegetarian, price=pizza.price)


@app.route("/create", methods=["POST"])
def create_pizza():
    data = request.json
    name = data["name"]
    vegetarian = data["vegetarian"]
    price = data["price"]

    try:
        save_new_pizza(name, vegetarian, price)
    except Exception as e:
        return make_response({"error": f"could not add pizza {str(e)}"}, 400)
    return make_response({"result": "success"}, 200)


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
    app.run()
