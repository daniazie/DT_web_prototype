from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager, current_user, AnonymousUserMixin
from control import post_control
from models import post

home_view = Blueprint("home_view", __name__)

@home_view.route("/home")
def home():
    posts = post_control.pull_post_from_db_rows(3)
    try:
        if current_user.id:
            print("logged in")
            return render_template("home-user.html",post_list=posts)
    except AttributeError:
        print("not logged in")
        return render_template("home-guest.html",post_list=posts)