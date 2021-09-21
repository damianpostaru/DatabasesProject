import pymysql

import db_config
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request


@app.route("/pizza")
def get_pizza():
    return "Hello World"


@app.route("/create", methods=["POST"])
def create_pizza():
    try:
        json = request.json
        name = json['name']
        vegetarian = json['vegetarian']
        price = json['price']
        if name is not None and vegetarian is not None and price is not None and request.method == 'POST':
            sql = "INSERT INTO pizzas(name, vegetarian, price) VALUES(%s, %s, %s)"
            data = (name, vegetarian, price)
            connexion = mysql.connect()
            cursor = connexion.cursor()
            cursor.execute(sql, data)
            connexion.commit()
            response = jsonify('Pizza added successfully!')
            response.status_code = 200
            return response
        else:
            return not_found()
    except Exception as e:
        print(e)


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
