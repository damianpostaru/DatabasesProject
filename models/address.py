from app import db


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(80), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.String(80), nullable=False)
    area = db.Column(db.String(80), nullable=False)