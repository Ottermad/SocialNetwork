# Models File

# Import Statements
from peewee import (
    SqliteDatabase,
    PostgresqlDatabase,
    Model,
    CharField,
    DateTimeField,
    BooleanField,
    IntegrityError,
    ForeignKeyField,
    TextField,
    DoesNotExist,
)
#from peewee import *
from flask.ext.login import (
    UserMixin,
)
from flask.ext.bcrypt import (
    generate_password_hash,
)
import os
import urllib.parse
import datetime


# Database Setup
# Check if deployed on Heroku
if "HEROKU" in os.environ:
    # If on heroku then create Postgres db
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

    # Database Configuration Dictionary
    database = {
        "engine": "peewee.PostgresqlDatabase",
        "name": url.path[1:],
        "user": url.username,
        "password": url.password,
        "host": url.hostname,
        "port": url.port
    }
    DATABASE = PostgresqlDatabase(
        database["name"],
        user=database["user"],
        password=database["password"],
        host=database["host"],
        port=database["port"]
    )
else:
    # Else create SQLite db
    DATABASE = SqliteDatabase("socialnetwork.db")


# User model
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("User already exists.")

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
    content=TextField()

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(rel_model=User)
    content = TextField()

class Comment(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(rel_model=User)
    post = ForeignKeyField(rel_model=Post)
    content = CharField()

def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Message, Post, Comment], safe=True)
    DATABASE.close()