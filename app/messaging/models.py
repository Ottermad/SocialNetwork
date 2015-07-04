from peewee import Model, DateTimeField, ForeignKeyField, TextField

from app.models import DATABASE
from app.user.models import User

import datetime

class Message(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    recipient = ForeignKeyField(
        rel_model=User,
        related_name="recipient"
    )
    sender = ForeignKeyField(
        rel_model=User,
        related_name="sender"
    )
    content = TextField()

    class Meta:
        database = DATABASE