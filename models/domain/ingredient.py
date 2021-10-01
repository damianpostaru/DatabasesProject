from models.mysql_model import db


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Ingredient {self.name}, vegetarian: {self.vegetarian}, with price {self.price}"
