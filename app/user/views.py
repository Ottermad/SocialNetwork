from flask import Blueprint, redirect, url_for, render_template, flash, request

from peewee import DoesNotExist

from flask.ext.bcrypt import check_password_hash

from flask.ext.login import login_user, login_required, logout_user, current_user, LoginManager

from app.user.forms import RegisterForm, LoginForm, BiographyForm
from app.user.models import User

from app.messaging.forms import MessagingForm
from app.posts.forms import PostForm

from app.functions import clean_markdown

import json
import html2text
import markdown
import hashlib



user_blueprint = Blueprint("user_blueprint", __name__)

h = html2text.HTML2Text()

@user_blueprint.route("/")
def index():
    if current_user.is_authenticated():
        return redirect(url_for(".home"))
    return render_template("index.html")

@user_blueprint.route("/home")
@login_required
def home():
    messaging_form = MessagingForm()
    post_form = PostForm()
    user = User.get(User.id == current_user.get_id())
    posts = user.get_posts()
    return render_template("home.html", messaging_form=messaging_form, post_form=post_form, posts=posts)


@user_blueprint.route("/register", methods=("POST", "GET"))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("a")
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        flash("You have registered")
        return redirect(url_for(".index"))
    return render_template("register.html", form=form)

@user_blueprint.route("/login", methods=("POST", "GET"))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password does not exist.")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in.")
                return redirect(url_for(".index"))
            else:
                flash("Your email or password does not exist.")
    return render_template("login.html", form=form)

@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for(".index"))

@user_blueprint.route("/create-bio", methods=("POST", "GET"))
@login_required
def create_bio():
    form = BiographyForm(request.form)
    if form.validate():
        user = User.get(User.id == current_user.get_id())
        md = form.biography.data
        cleaned_markdown = clean_markdown(md)
        html = markdown.markdown(cleaned_markdown)
        result = user.create_bio(html)
        return result
    else:
        return form.errors

@user_blueprint.route("/get-bio", methods=("POST", "GET"))
@login_required
def get_bio():
    user = User.get(User.id == current_user.get_id())
    bio = user.get_bio()
    bio_md = h.handle(bio[0])
    return json.dumps([bio_md, bio[0]])

def gravatar_hash(email):
    email = email.strip()
    email = email.lower()
    email = email.encode()
    email_hash = hashlib.md5(email).hexdigest()
    return email_hash
    
@user_blueprint.route("/friend-request", methods=("POST", "GET"))
@login_required
def friend_request():
    username = request.form["username"]
    print("USERNAME:", username)
    user = User.get(User.id == current_user.get_id())
    response = user.friend_request(username)
    return response

@user_blueprint.route("/view-friend-requests")
@login_required
def view_friend_requests():
    user = User.get(User.id == current_user.get_id())
    requests = user.get_friend_requests()
    return render_template("view_friend_requests.html", requests=requests)

@user_blueprint.route("/get-friend-requests", methods=("POST", "GET"))
@login_required
def get_friend_requests():
    user = User.get(User.id == current_user.get_id())
    requests = user.get_friend_requests()
    return json.dumps(requests)

@user_blueprint.route("/confirm-friend-request", methods=("POST", "GET"))
@login_required
def confirm_friend_request():
    id = request.form["id"]
    if request.form["result"] == "True":
        result = True
    else:
        result = False
    response = User.confirm_friend_request(id, result)
    return response

@user_blueprint.route("/user/<username>")
@login_required
def user(username):
   try:
        other_user = User.get(User.username == username)
        bio_form = BiographyForm()
        user = User.get(User.id == current_user.get_id())
        other_user_email = other_user.email
        other_user_email_hash = gravatar_hash(other_user_email)
        gravatar = "http://www.gravatar.com/avatar/{}?s=300".format(other_user_email_hash)
        data = User.view_user(username)
        is_pending = user.is_pending(username)
        is_friend = user.is_friend(username)
        if user.username == username:
            own_page = True
        else:
            own_page = False
        print("IS PENDING:", is_pending, "IS FRIEND:", is_friend)
        return render_template("user.html", user=data, is_friend=is_friend, is_pending=is_pending, own_page=own_page, gravatar=gravatar, bio_form=bio_form)
   except DoesNotExist:
    return render_template("error.html", title="User does not exist.", description="Please make sure the url contains a valid username.")

@user_blueprint.route("/user-listing")
@login_required
def user_listing():
    users = User.get_all_users()
    return render_template("user-listing.html", users=users)