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

import forms
import models

# Set up application - need a secret key for secure sessions
app = Flask(__name__)
app.secret_key = open("key.txt").readline()

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Login Manager Functions

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None

# Before and After request functions

@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

# Routes

@app.route("/register", methods=("POST", "GET"))
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        flash("You have registered")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)
