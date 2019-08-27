from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    username = pw.CharField(unique=True)

