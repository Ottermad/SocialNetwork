from peewee import Model, DateTimeField, ForeignKeyField, TextField, CharField
from app.models import DATABASE
from app.user.models import User

import datetime

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(rel_model=User)
    content = TextField()

    @classmethod
    def get_post(cls, post_id):
        post = Post.get(Post.id == post_id)

        data = [post.user.username, post.timestamp.strftime("%H:%M %d/%m/%y"), post.content]
        comment_query = Comment.select().where(Comment.post == post).order_by(Comment.timestamp.asc())
        comments = []
        for comment in comment_query:
            print(comment.__dict__)
            commenter = User.get(User.id == comment.user)
            comment_data = [commenter.username, comment.timestamp.strftime("%H:%M %d/%m/%y"), comment.content]
            comments.append(comment_data)
        data.append(comments)
        data.append(post.id)
        return data

    class Meta:
        database = DATABASE

class Comment(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(rel_model=User)
    post = ForeignKeyField(rel_model=Post)
    content = CharField()

    class Meta:
        database = DATABASE