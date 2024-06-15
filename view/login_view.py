from flask import Flask, request, url_for, redirect, session, render_template, Blueprint
from flask_login import login_user, LoginManager, logout_user
import control.user_control as user_control
from control.messages_control import count_unread_messages
import models.user as user

login_view = Blueprint("login_view", __name__)

login_manager = LoginManager()

@login_view.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_view.route("/login", methods = ['GET', 'POST'])
def login():
    logout_user()
    if request.method == "POST":
        user_id = request.form.get('Username')
        user_pw = request.form.get('Password')

        if user_control.is_empty(user_id,user_pw):
            return render_template('login.html')

        user_info = user.User()
        
        user_info = user_control.pull_user_info_from_db(user_id)
        if user_info != None:
            if user_control.check_password(user_info, user_pw):
                user_info.message_to_read = count_unread_messages(user_id)
                login_user(user_info)
                return redirect('/home')
            else:
                message = "Wrong password."
                return render_template('login.html', message=message)
        if user_info is None: 
            message = "No account with that username exists."
            return render_template('login.html', message=message)
    return render_template('login.html')

@login_manager.user_loader
def user_loader(user_id):
    user_info = user_control.pull_user_info_from_db(user_id)
    user_info.message_to_read = count_unread_messages(user_id)
    return user_info

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")