from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager

posts_view = Blueprint("posts_view", __name__)

@posts_view.route("/posts")
@login_required
def home():
    return render_template("posts.html")