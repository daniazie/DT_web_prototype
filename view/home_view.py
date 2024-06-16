from flask import Flask, request, session, render_template, Blueprint
from flask_login import  current_user
from models.socketio import socketio
from control import lang_control, post_control
from models import post

home_view = Blueprint("home_view", __name__)

@home_view.record_once
def on_load(state):
    socketio.init_app(state.app, cors_allowed_origins="*")

@home_view.route("/home")
def home():
    labels = lang_control.load_lang_dict("home",lang_control.selected_lang)
    posts = post_control.pull_post_from_db_rows(3)
    
    try:
        if current_user.id:
            return render_template("home-user.html",post_list=posts,labels=labels,user=current_user)
    except AttributeError as e:
        return render_template("home-guest.html",post_list=posts,labels=labels)

@socketio.on('lang_selected')
def lang_selected(data):
    lang_control.selected_lang = data.get("lang")
