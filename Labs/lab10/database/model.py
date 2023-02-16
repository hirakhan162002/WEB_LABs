from .db import  db

class Product(db.Document):
        name = db.StringField(required=True)
        description = db.StringField(required=True)
        price = db.FloatField()