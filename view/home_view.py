from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager

home_view = Blueprint("home_view", __name__)

@home_view.route("/home")
@login_required
def home():
    return render_template("home.html")