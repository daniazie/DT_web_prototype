from flask import Flask, flash, redirect, request, render_template, Blueprint, session
from flask_login import current_user
from control import user_control
from models import user

edit_profile_view = Blueprint("edit_profile_view", __name__)

@edit_profile_view.route("/edit-profile", methods = ['GET', 'POST'])
def edit():
    if request.method == "POST":
        input_name = request.form.get('name')
        input_gender = request.form.get('gender')
        input_language = request.form.get('language')
        input_city = request.form.get('city')
        print(input_name,input_gender,input_language,input_city)
        flag_empty = user_control.is_empty(input_name, input_gender,
                                           input_language, input_city)
        
        if flag_empty:
            return render_template("/my-profile-edit.html")
        
        user_info = user.User()
        user_info.id = current_user.id
        user_info.email = current_user.email
        user_info.password = current_user.password
        user_info.country = current_user.country
        user_info.name = input_name
        user_info.gender = input_gender
        user_info.language = input_language
        user_info.city = input_city

        if not user_control.push_user_info_to_db(user_info) :
            flash("ERR_CODE:FAILED_TO_PUSH_DB",category="error")

        return redirect("/my_profile")
    else:
        return render_template("/my-profile-edit.html")