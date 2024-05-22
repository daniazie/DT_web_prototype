from flask import Flask, request, url_for, redirect, session, render_template, Blueprint
from flask_login import login_user, LoginManager
import control.login_control as login_control
import models.user as user

login_view = Blueprint("login_view", __name__)

login_manager = LoginManager()

@login_view.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_view.route("/login", methods = ['GET', 'POST'])
def login():
    user_id = request.form.get('Username')
    user_pw = request.form.get('Password')

    if user_id is None or user_pw is None:
        return render_template('login.html')

    user_info = user.User()
    
    flag = user_info.set_info_from_database_by_id(user_id)
    if flag:
        if user_info.check_password(user_pw):
            login_user(user_info)
            return redirect('/index')

    return render_template('login.html')

@login_manager.user_loader
def user_loader(user_id):
    user_info = user.User()
    user_info.set_info_from_database_by_id(user_id)
    return user_info

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")