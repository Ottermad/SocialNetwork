# Models File

# Import Statements
from peewee import (
    SqliteDatabase,
    PostgresqlDatabase,
)

from app.config import PATH

import os
import urllib.parse
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
    DATABASE = SqliteDatabase(PATH + "socialnetwork.db")


def initialise():
    from app.user.models import User, Friends
    from app.posts.models import Post, Comment
    from app.messaging.models import Message
    from app.bugreport.models import BugReport
    DATABASE.connect()
    DATABASE.create_tables([User, Message, Post, Comment, Friends, BugReport], safe=True)
    DATABASE.close()
