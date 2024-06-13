from flask import Flask, url_for, redirect, render_template, Blueprint, request, session
from flask_login import login_required, login_manager, current_user
from models import language

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile", methods=['GET'])
@login_required
def home():
    name = current_user.name
    gender = current_user.gender
    lang = language.convert_code_to_lang(current_user.language,type="NA")
    country = current_user.country
    city = current_user.city
    return render_template("my-profile.html", name=name, gender=gender, language=lang, country=country, city=city)