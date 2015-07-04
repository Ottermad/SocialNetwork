from peewee import Model, ForeignKeyField, TextField, DateTimeField, BooleanField
from app.models import DATABASE
from app.user.models import User

import datetime

class BugReport(Model):
    user = ForeignKeyField(rel_model=User)
    description = TextField()
    datetime = DateTimeField(default=datetime.datetime.now)
    seen = BooleanField(default=False)
    class Meta:
        database = DATABASE