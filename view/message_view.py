from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, login_manager

message_view = Blueprint("message_view", __name__)

@message_view.route("/message")
@login_required
def home():
    return render_template("message.html")