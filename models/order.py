from app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(80), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_number = db.Column(db.String(80), nullable=False, unique=True)
    order_time = db.Column(db.DateTime, nullable=False)
    pizzas = db.relationship('Pizza', secondary='order_content', backref='order_pizza', lazy=True)
    desserts = db.relationship('Dessert', secondary='order_content', backref='order_dessert', lazy=True)
    drinks = db.relationship('Drink', secondary='order_content', backref='order_drink', lazy=True)


db.create_all()
