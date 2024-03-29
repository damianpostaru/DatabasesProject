from app import db

pizza_ingredients = db.Table('pizza_ingredients',
                             db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id')),
                             db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')))


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.relationship(
        'Ingredient', secondary=pizza_ingredients,
        backref=db.backref('ingredients', lazy='dynamic')
    )

    @staticmethod
    def deserialize(pizza_d: dict):
        return Pizza(**pizza_d)

    def __repr__(self):
        return f"name: {self.name}, id: {self.id}, vegetarian: {self.vegetarian}, price: {self.price}"
