# Main File for Application

# Import Statements
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    g,
    flash,
    request,
)

from flask.ext.bcrypt import (
    check_password_hash,
)

from flask.ext.login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)


