from flask import Blueprint, render_template, redirect, url_for, flash
from flask.ext.login import (
    login_required,
    current_user
)

from app.bugreport.forms import BugReportForm
from app.user.models import User

bugreport_blueprint = Blueprint("bugreport_blueprint", __name__)

@bugreport_blueprint.route("/report", methods=("POST", "GET"))
@login_required
def report():
    form = BugReportForm()
    if form.validate_on_submit():
        # Do Stuff
        description = form.description.data
        user = User.get(User.id == current_user.get_id())
        result = user.file_bug_report(description)
        flash(result)
        return redirect(url_for("home"))
    return render_template("bugreport/report.html", form=form)
