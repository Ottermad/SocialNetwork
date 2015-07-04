from flask_wtf import (
    Form,
)

from wtforms import (
    TextAreaField,
)

from wtforms.validators import (
    DataRequired,

)

class BugReportForm(Form):
    description = TextAreaField("description", validators=[DataRequired()])