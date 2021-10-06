from app import db


class OrderItem(db.Model):
    menu_item = db.Column(db.Integer, db.ForeignKey("menu_item.id"), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, primary_key=True)
