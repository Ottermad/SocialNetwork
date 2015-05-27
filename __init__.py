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

from peewee import (
    DoesNotExist
)

import forms
import models
import os
import json
import re
import markdown

# Set up application - need a secret key for secure sessions
app = Flask(__name__)
app.secret_key = open("key.txt").readline()

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Functions
def clean_markdown(raw_md):
    cleanr = re.compile("<.*?>")
    cleaned_md = re.sub(cleanr, "", raw_md)
    return cleaned_md

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

@app.route("/")
def index():
    if current_user.is_authenticated():
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    messaging_form = forms.MessagingForm()
    post_form = forms.PostForm()
    user = models.User.get(models.User.id == current_user.get_id())
    posts = user.get_posts()
    return render_template("home.html", messaging_form=messaging_form, post_form=post_form, posts=posts)


@app.route("/register", methods=("POST", "GET"))
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        print("a")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        flash("You have registered")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)

@app.route("/login", methods=("POST", "GET"))
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password does not exist.")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in.")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not exist.")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))

@app.route("/get-messages", methods=("POST", "GET"))
@login_required
def get_messages():
    user = models.User.get(models.User.id == current_user.get_id())
    other = models.User.get(models.User.username == request.form["other"])
    json_messages = json.dumps(user.get_messages(other))
    return json_messages

@app.route("/send-message", methods=("POST", "GET"))
@login_required
def send_message():
    # get form
    form = forms.MessagingForm(request.form)
    if form.validate():
        # Send message
        print("sending")
        user = models.User.get(models.User.id == current_user.get_id())
        result = user.send_message(form.recipient.data, form.body.data)
        return result
    else:
        print(form.errors)
        return "Validation Error."

@app.route("/people", methods=("POST", "GET"))
@login_required
def people():
    user = models.User.get(models.User.id == current_user.get_id())
    json_people = json.dumps(user.get_people())
    return json_people

@app.route("/get-posts", methods=("POST", "GET"))
@login_required
def get_posts():
    offset = request.form["offset"]
    user = models.User.get(models.User.id == current_user.get_id())
    posts = json.dumps(user.get_posts(offset=int(offset)))
    return posts

@app.route("/add-post", methods=("POST", "GET"))
@login_required
def add_post():
    form = forms.PostForm(request.form)
    if form.validate():
        user = models.User.get(models.User.id == current_user.get_id())
        md = form.post.data
        cleaned_markdown = clean_markdown(md)
        html = markdown.markdown(cleaned_markdown)
        result = user.create_post(html)
        return result
    else:
        return form.errors

@app.route("/comment", methods=("POST", "GET"))
@login_required
def comment():
    form = forms.CommentForm(request.form)
    print(request.form)
    if form.validate():
        user = models.User.get(models.User.id == current_user.get_id())
        comment_text = form.comment.data
        post_id = form.post_id.data
        result = user.comment(post_id, comment_text)
        return result
    return form.errors

@app.route("/get-post", methods=("POST", "GET"))
@login_required
def get_post():
    id = request.form["id"]
    post = models.Post.get_post(id)
    post = json.dumps(post)
    return post

@app.route("/user/<username>")
@login_required
def user(username):
    data = models.User.view_user(username)
    return render_template("user.html", user=data)

@app.route("/friend-request", methods=("POST", "GET"))
@login_required
def friend_request():
    username = request.form["username"]
    print("USERNAME:", username)
    user = models.User.get(models.User.id == current_user.get_id())
    response = user.friend_request(username)
    return response

@app.route("/view-friend-requests")
@login_required
def view_friend_requests():
    user = models.User.get(models.User.id == current_user.get_id())
    requests = user.get_friend_requests()
    return render_template("view_friend_requests.html")

try:
    models.initialise()
except:
    None


if "HEROKU" not in os.environ:
    if __name__ == "__main__":
        app.run(debug=True)
