from flask import Flask, request, session, render_template, Blueprint
from flask_login import  current_user
from control import lang_control, post_control, community_control
from models import post

home_view = Blueprint("home_view", __name__)

@home_view.route("/home")
def home():
    labels = lang_control.load_lang_dict("home",lang_control.selected_lang)
    posts = post_control.pull_post_from_db_rows(3)
    
    try:
        if current_user.id:
            my_comm_list = community_control.pull_community_list_from_db(current_user.id)
            sug_comm_list = community_control.get_suggested_community_list(current_user.id,2)
            return render_template("home/home-user.html",post_list=posts,labels=labels,user=current_user,
                                   my_comm_list=my_comm_list[:2],sug_comm_list=sug_comm_list)
    except AttributeError as e:
        return render_template("home/home-guest.html",post_list=posts,labels=labels)
    