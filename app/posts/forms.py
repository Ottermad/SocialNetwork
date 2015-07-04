from flask_wtf import (
    Form,
)

from wtforms import (
    StringField,
    TextAreaField,
    IntegerField
)

from wtforms.validators import (
    DataRequired,

)


class PostForm(Form):
    post = TextAreaField("post", id="wmd-input", validators=[DataRequired()])


class CommentForm(Form):
    comment = StringField("comment", validators=[DataRequired()])
    post_id = IntegerField("postid", validators=[DataRequired()])