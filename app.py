from flask import Flask

app = Flask(__name__)


@app.route("/pizza")
def get_pizza():
    return "Hello World"
