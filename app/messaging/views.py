from flask import Blueprint, request

from flask.ext.login import login_required, current_user

from app.messaging.forms import MessagingForm

from app.user.models import User

import json

messaging_blueprint = Blueprint("messaging_blueprint", __name__)

@messaging_blueprint.route("/get-messages", methods=("POST", "GET"))
@login_required
def get_messages():
    user = User.get(User.id == current_user.get_id())
    other = User.get(User.username == request.form["other"])
    json_messages = json.dumps(user.get_messages(other))
    return json_messages

@messaging_blueprint.route("/send-message", methods=("POST", "GET"))
@login_required
def send_message():
    # get form
    form = MessagingForm(request.form)
    if form.validate():
        # Send message
        print("sending")
        user = User.get(User.id == current_user.get_id())
        result = user.send_message(form.recipient.data, form.body.data)
        return result
    else:
        print(form.errors)
        return "Validation Error."

@messaging_blueprint.route("/people", methods=("POST", "GET"))
@login_required
def people():
    user = User.get(User.id == current_user.get_id())
    json_people = json.dumps(user.get_people())
    return json_people