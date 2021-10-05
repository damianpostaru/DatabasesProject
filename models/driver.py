from app import db


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    working_area = db.Column(db.String(80), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
