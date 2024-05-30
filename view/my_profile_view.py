from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile")
@login_required
def home():
    return render_template("my-profile.html")