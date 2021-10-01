from modules.mysql_model import db

order_content = db.Table('order_content',
                         db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True, nullable=False),
                         db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'), primary_key=True, nullable=False),
                         db.Column('dessert_id', db.Integer, db.ForeignKey('dessert.id'), primary_key=True),
                         db.Column('drink_id', db.Integer, db.ForeignKey('drink.id'), primary_key=True)
                         )

db.create_all()
