from app import db


# pizzas = db.Table('pizzas',
#                   db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'), primary_key=True),
#                   db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)
#                   )


class Pizzas(db.Model):
    __tablename__ = 'pizzas'
    pizza_id = db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'), primary_key=True)
    order_id = db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # address = db.Column(db.String(80), nullable=False)
    # customer_name = db.Column(db.String(120), nullable=False)
    # customer_number = db.Column(db.String(80), nullable=False, unique=True)
    # order_time = db.Column(db.DateTime, nullable=False)
    # order_content = db.Column(db.Integer, db.ForeignKey('order_content.id'))
    pizzas = db.relationship('Pizza', secondary="pizzas", backref='pizzas')


db.create_all()
