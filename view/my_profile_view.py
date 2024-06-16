from flask import Flask, url_for, redirect, render_template, Blueprint, request, session
from flask_login import login_required, login_manager, current_user
from control import lang_control
from models import language

my_profile_view = Blueprint("my_profile_view", __name__)

@my_profile_view.route("/my_profile", methods=['GET'])
@login_required
def home():
    labels = lang_control.load_lang_dict("my-profile",lang_control.selected_lang)
    lang = language.convert_code_to_lang(current_user.language,type="NA")
    return render_template("my-profile.html", user=current_user, lang=lang, labels=labels)