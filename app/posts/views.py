from flask import Blueprint, request

from flask.ext.login import login_required, current_user

import json
import markdown

from app.functions import clean_markdown
from app.posts.forms import PostForm, CommentForm

from app.user.models import User
from app.posts.models import Post

posts_blueprint = Blueprint("posts_blueprint", __name__)

@posts_blueprint.route("/get-posts", methods=("POST", "GET"))
@login_required
def get_posts():
    offset = request.form["offset"]
    user = User.get(User.id == current_user.get_id())
    posts = json.dumps(user.get_posts(offset=int(offset)))
    return posts

@posts_blueprint.route("/add-post", methods=("POST", "GET"))
@login_required
def add_post():
    form = PostForm(request.form)
    if form.validate():
        user = User.get(User.id == current_user.get_id())
        md = form.post.data
        cleaned_markdown = clean_markdown(md)
        html = markdown.markdown(cleaned_markdown)
        result = user.create_post(html)
        return result
    else:
        return form.errors

@posts_blueprint.route("/comment", methods=("POST", "GET"))
@login_required
def comment():
    form = CommentForm(request.form)
    print(request.form)
    if form.validate():
        user = User.get(User.id == current_user.get_id())
        comment_text = form.comment.data
        post_id = form.post_id.data
        result = user.comment(post_id, comment_text)
        return result
    return form.errors

@posts_blueprint.route("/get-post", methods=("POST", "GET"))
@login_required
def get_post():
    id = request.form["id"]
    post = Post.get_post(id)
    post = json.dumps(post)
    return post

@posts_blueprint.route("/delete-post", methods=("POST", "GET"))
@login_required
def delete_post():
    user = User.get(User.id == current_user.get_id())
    post_id = request.form["id"]
    result = user.delete_post(post_id)    
    return result

@posts_blueprint.route("/edit-post", methods=("POST", "GET"))
@login_required
def edit_post():
    user = User.get(User.id == current_user.get_id())
    post_id = request.form["id"]
    content = request.form["content"]
    cleaned_markdown = clean_markdown(content)
    html = markdown.markdown(cleaned_markdown)
    result = user.edit_post(post_id, html)
    return result