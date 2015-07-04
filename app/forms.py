from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
)

from wtforms.validators import (
    DataRequired,
    Regexp,
    ValidationError,
    Email,
    Length,
    EqualTo,
)

from app.user.models import (
    User,
)

def username_exists(form, field):
    if not User.select().where(User.username == field.data).exists():
        raise ValidationError("User does not exist.")
