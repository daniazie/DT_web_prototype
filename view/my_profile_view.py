from flask import Flask, url_for, redirect, render_template, Blueprint, request, session
from flask_login import login_required, login_manager, current_user
from control import user_control

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile", methods=['GET'])
@login_required
def home():
    user_id = current_user.id
    user_info = user_control.pull_user_info_from_db(user_id)
    name = current_user.name
    gender = current_user.gender
    language = current_user.language
    country = current_user.country
    city = current_user.city
    print(name, gender, language, city)
    return render_template("my-profile.html", name=name, gender=gender, language=language, country=country, city=city)