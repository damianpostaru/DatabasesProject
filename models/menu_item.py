from app import db


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=True, unique=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=True, unique=True)
    dessert_id = db.Column(db.Integer, db.ForeignKey('dessert.id'), nullable=True, unique=True)
    order_items = db.relationship("OrderItem", backref='menu_ordered_item')
