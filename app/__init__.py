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

from flask.ext.login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.config import PATH, DEBUG

from app.posts.forms import PostForm
from app.messaging.forms import MessagingForm

from app.user.models import User

import os
import json
import re
import markdown
import hashlib
import html2text

from app.models import DATABASE


h = html2text.HTML2Text()


# Set up application - need a secret key for secure sessions
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', None)
app.config["DEBUG"] = bool(os.environ.get('DEBUG', False))


# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_blueprint.login"


# Login Manager Functions

@login_manager.user_loader
def load_user(userid):
    """Load user based on id for flask-login."""
    try:
        return User.get(User.id == userid)
    except:
        return None


# Before and After request functions
@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

# Routes

from app.user.views import user_blueprint
from app.posts.views import posts_blueprint
from app.messaging.views import messaging_blueprint
from app.bugreport.views import bugreport_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(messaging_blueprint)
app.register_blueprint(bugreport_blueprint)
