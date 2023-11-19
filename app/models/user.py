from mongoengine import *
from app.db.db import uri
# Interfaces

USER_COLLECTION = 'users'

connect(host=uri)


class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True, max_length=100)
    date = DateField(required=True)
