# models.py
from peewee import Model, CharField, IntegerField
from db import db

class Order(Model):
    name = CharField()
    quantity = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Order])
