from playhouse.migrate import *
from models import DATABASE, User

migrator = SqliteMigrator(DATABASE)

migrate(
    migrator.add_column("user", "biography", User.biography)
)

