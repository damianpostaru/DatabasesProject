from app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(80), nullable=False)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_number = db.Column(db.String(80), nullable=False, unique=True)
    status = db.Column(db.String(80), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    order_items = db.relationship("OrderItem", backref='order')


db.create_all()
