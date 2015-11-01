from peewee import Model, CharField, ForeignKeyField
from app.models import DATABASE


class Group(Model):
    name = CharField(unique=True)
    group_type = ForeignKeyField(rel_model=GroupType)


class GroupType(Model):
    name = CharField(unique=True)

    class Meta:
        database = DATABASE


class UserGroups(Model):
    pass
