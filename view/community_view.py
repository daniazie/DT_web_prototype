from flask import Flask, url_for, redirect, render_template, Blueprint
from flask_login import login_required, current_user
from control import lang_control

community_view = Blueprint("community_view", __name__)

@community_view.route("/community")
@login_required
def home():
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)
    return render_template("community/community.html",user=current_user,labels=labels)