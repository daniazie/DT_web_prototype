from flask import Flask, request, session, render_template, Blueprint
from flask_login import login_required, login_manager, current_user, AnonymousUserMixin
from control import post_control, util
from models import post

home_view = Blueprint("home_view", __name__)

@home_view.route("/home")
def home():
    lang = "en"
    if 'selected_lang' in session:
        lang = session['selected_lang']

    labels = util.load_lang_dict("home",lang)
    posts = post_control.pull_post_from_db_rows(3)
    
    try:
        if current_user.id:
            return render_template("home-user.html",post_list=posts,labels=labels,user=current_user)
    except AttributeError as e:
        return render_template("home-guest.html",post_list=posts,labels=labels)
    
@home_view.route("/home", methods=['POST'])
def select_lang():
    selected_lang = "en"
    try:
        data = request.json
        selected_lang = data.get('lang')
    except:
        selected_lang = "en"

    session['selected_lang']=selected_lang

    return home()