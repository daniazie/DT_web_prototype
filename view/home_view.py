from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager
from control import post_control
from models import post


home_view = Blueprint("home_view", __name__)

@home_view.route("/home")
@login_required
def home():
    posts = post_control.pull_post_from_db_rows(3)
    return render_template("home.html",list=posts)