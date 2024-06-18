from flask import Flask, request, redirect, render_template, Blueprint, flash
from flask_login import login_required, current_user
from control import lang_control, community_control
from models.socketio import socketio

community_view = Blueprint("community_view", __name__)

@community_view.route("/community")
@login_required
def home():
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)
    my_comm_list = community_control.pull_community_list_from_db(current_user.id)
    sug_comm_list = community_control.get_suggested_community_list(current_user.id,3)
    return render_template("community/community.html",user=current_user,labels=labels,
                           my_comm_list=my_comm_list,sug_comm_list=sug_comm_list)

@community_view.route("/community/comm")
@login_required
def comm():
    community_id = request.args.get('id')
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)
    community = community_control.pull_community_from_db(community_id)
    return render_template("community/community-posts.html",user=current_user,labels=labels,
                           community=community)

@community_view.route("/community/join")
@login_required
def comm_join():
    community_id = request.args.get('id')
    if community_control.join_community(community_id,current_user.id):
        flash("SUC_CODE:POST_UPLOADED", category='success')
    else:
        flash("ERR_CODE:FAILED_TO_JOIN_COMM", category='error')

    return redirect("/community")