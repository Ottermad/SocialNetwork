from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,

)

from app.forms import username_exists

class MessagingForm(Form):
    recipient = StringField("Recipient", validators=[DataRequired(), username_exists])
    body = TextAreaField("Body", validators=[DataRequired()])