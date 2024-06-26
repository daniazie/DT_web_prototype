from flask import Flask, url_for, redirect, render_template, Blueprint, request, session
from flask_login import login_required, login_manager, current_user

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile", methods=['GET'])
@login_required
def home():
    name = current_user.name
    gender = current_user.gender
    language = current_user.language
    country = current_user.country
    city = current_user.city
    return render_template("my-profile.html", name=name, gender=gender, language=language, country=country, city=city)