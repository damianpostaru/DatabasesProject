from app import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Ingredient {self.name}, vegetarian: {self.vegetarian}, with price {self.price}"
