from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,
    Regexp,
    ValidationError,
    Email,
    Length,
    EqualTo,
)

from models import (
    User,
)


def username_exists(form, field):
    if not User.select().where(User.username == field.data).exists():
        raise ValidationError("User does not exist.")


def username_in_use(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("Username already in use.")


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Email already in use.")


class RegisterForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message="Usernames should be one word, with letters, numbers and underscores only."
            ),
            username_in_use,
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo("password2", message="Passwords must match.")
        ]
    )
    password2 = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
        ]
    )


class LoginForm(Form):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class MessagingForm(Form):
    recipient = StringField("Recipient", validators=[DataRequired(), username_exists])
    body = TextAreaField("Body", validators=[DataRequired()])

class PostForm(Form):
    post = TextAreaField("post", id="wmd-input", validators=[DataRequired()])

class CommentForm(Form):
    comment = StringField("comment", validators=[DataRequired()])