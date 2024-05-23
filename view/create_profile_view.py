from flask import Flask, flash, redirect, request, render_template, Blueprint, session
from control import user_control
from models import user

create_profile_view = Blueprint("create_profile_view", __name__)

@create_profile_view.route("/create-profile", methods = ['GET', 'POST'])
def singup():
    if 'user_id_temp' in session or \
     'user_email_temp'in session or \
     'user_password_temp'in session or \
     'user_country_temp': 
        redirect("/signup")
    

    if request.method == "POST":
        input_name = request.form.get('name')
        input_gender = request.form.get('gender')
        input_language = request.form.get('language')
        input_city = request.form.get('city')
        print(input_name,input_gender,input_language,input_city)
        flag_empty = user_control.is_empty(input_name, input_gender,
                                           input_language, input_city)
        
        if flag_empty:
            return render_template("/create-profile.html")
        
        user_info = user.User()
        user_info.id = session['user_id_temp']
        user_info.email = session['user_email_temp']
        user_info.password = session['user_password_temp']
        user_info.country = session['user_country_temp']
        user_info.name = input_name
        user_info.gender = input_gender
        user_info.language = input_language
        user_info.city = input_city

        user_control.push_user_info_to_db(user_info)

        session.pop('user_id_temp',None)
        session.pop('user_email_temp',None)
        session.pop('user_password_temp',None)
        session.pop('user_country_temp',None)

        return redirect("/login")
    else:
        return render_template("/create-profile.html")