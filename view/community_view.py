from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager

community_view = Blueprint("community_view", __name__)

@community_view.route("/community")
@login_required
def home():
    return render_template("community.html")