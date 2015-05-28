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
    biography = TextField(null=True)

    class Meta:
        database = DATABASE

    def get_messages(self, other):
        query = Message.select().where(
            (
                (Message.recipient == self.id) | (Message.sender == self.id)
            ) & (
                (Message.recipient == other.id) | (Message.sender == other.id)
            )
        ).order_by(Message.timestamp.asc())
        messages = []
        for message in query:
            item = [message.content, message.timestamp.strftime("%H:%M %d/%m/%y")]
            if message.sender.id != self.id:
                item.append(False)
            elif message.recipient.id != self.id:
                item.append(True)

            messages.append(item)
        return messages

    def get_people(self):
        query = User.select()
        usernames = []
        for user in query:
            print(user.id, self.id)
            if user.id != self.id:
                usernames.append(user.username)
        return usernames

    def send_message(self, recipient_name, message_body):
        recipient = User.get(User.username == recipient_name)
        try:
            Message.create(sender=self, recipient=recipient, content=message_body)
            return "Message sent."
        except:
            return "There was an error sending the message."

    def get_posts(self, number=10, offset=0):
        query = Post.select().order_by(Post.timestamp.desc()).limit(number).offset(offset)
        posts = []
        for post in query:
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
            posts.append(data)
        return posts

    def create_post(self, content):
        try:
            Post.create(
                user=self,
                content=content
            )
            return "Posted!"
        except:
            return "There was an error posting your post."

    def comment(self, post_id, comment_text):
        post = Post.get(Post.id == post_id)
        print(comment_text)
        try:
            Comment.create(
                user=self,
                post=post,
                content=comment_text
            )
            return "Commented."
        except:
            return "Error commenting."

    def friend_request(self, username):
        user = User.get(User.username == username)
        request = Friends.create(
            user1=self,
            user2=user
        )
        return "Sent."

    def get_friend_requests(self):
        query = Friends.select().where((Friends.user2 == self) & (Friends.confirmed == -1))
        requests = []
        for request in query:
            other = User.get(User.id == request.user1.id)
            data = [other.username, request.id]
            requests.append(data)
        return requests

    def is_friend(self, username):
        other = User.get(User.username == username)
        is_friend = Friends.select().where(
            (
                (Friends.user1 == self & Friends.user2 == other) | (Friends.user1 == other & Friends.user2 == self)
            ) & (
                Friends.confirmed == 1
            )
        ).exists()
        return is_friend

    def is_pending(self, username):
        other = User.get(User.username == username)
        is_friend = Friends.select().where(
            (
                (Friends.user1 == self & Friends.user2 == other) | (Friends.user1 == other & Friends.user2 == self)
            ) & (
                Friends.confirmed == -1
            )
        ).exists()
        return is_friend

    def create_bio(self, bio):
        try:
            self.biography = bio
            self.save()
            return "Done."
        except:
            return "Error"



    @classmethod
    def confirm_friend_request(cls, id, answer):
        try:
            request = Friends.get(Friends.id == id)
            if answer is True:
                request.confirmed = 1
            else:
                request.confirmed = 0
            request.save()
            return "Done."
        except:
            return "Error"

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

    @classmethod
    def view_user(cls, username):
        user = User.get(User.username == username)
        data = {"id": user.id, "username": user.username, "biography": user.biography}
        return data

    @classmethod
    def get_all_users(cls):
        query = User.select()
        data = []
        for user in query:
            data.append(user.username)
        return data

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

class Friends(Model):
    user1 = ForeignKeyField(rel_model=User, related_name="user1")
    user2 = ForeignKeyField(rel_model=User, related_name="user2")
    confirmed = IntegerField(default=-1)

    class Meta:
        database = DATABASE

def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Message, Post, Comment, Friends], safe=True)
    DATABASE.close()