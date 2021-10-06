from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    orders = db.relationship("Order", backref='customer')
