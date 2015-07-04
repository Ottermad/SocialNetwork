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
    IntegerField
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
import html2text

h = html2text.HTML2Text()

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



"""
def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Message, Post, Comment, Friends, BugReport], safe=True)
    DATABASE.close()
"""