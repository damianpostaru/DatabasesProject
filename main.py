import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request


@app.route("/pizza")
def get_pizza():
    return "Hello World"


@app.route("/create", methods=["POST"])
def create_pizza():
    return "Good"


@app.route("/add", methods=['POST'])
def add_user():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']
        print(_name)
        # validate the received values
        if _name and _email and _password and request.method == 'POST':
            # do not save password as a plain text
            # save edits
            sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
            data = (_name, _email, _password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 405,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    app.run()
