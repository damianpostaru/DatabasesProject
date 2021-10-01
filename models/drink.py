from app import db


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)


db.create_all()
