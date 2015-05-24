from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    PasswordField,
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
    if User.select().where(User.username == field.data).exists():
        raise ValidationError("Username already in use.")

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError("Email already in use.")

class SignUpForm(Form):
    username = StringField(
        "Username",
        validators=[
            DataRequired,
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message="Usernames should be one word, with letters, numbers and underscores only."
            ),
            username_exists,
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired,
            Email(),
            email_exists()
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
