from flask import Flask, url_for, redirect, render_template, Blueprint, request, session
from flask_login import login_required, login_manager, current_user
from control import lang_control
from models import language

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile", methods=['GET'])
@login_required
def home():
    labels = lang_control.load_lang_dict("my-profile")
    lang = language.convert_code_to_lang(current_user.language,type="EN")
    translated_user = lang_control.translate_profile(current_user)
    return render_template("my_profile/my-profile.html", user=translated_user, labels=labels)