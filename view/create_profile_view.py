from flask import Flask, flash, redirect, request, render_template, Blueprint, session
from control import lang_control, user_control
from models import user

create_profile_view = Blueprint("create_profile_view", __name__)

@create_profile_view.route("/create-profile", methods = ['GET', 'POST'])
def singup():
    labels = lang_control.load_lang_dict("create-profile")
    try:
        sessionFlag = 'user_id_temp' in session and \
        'user_email_temp'in session and \
        'user_password_temp'in session and \
        'user_country_temp' in session and \
            'user_websocket_id_temp'
        
        if not sessionFlag :
            flash("ERR_CODE:USER_INFO_LOST",category="error")
            return redirect("/signup")
    except:
        flash("ERR_CODE:USER_INFO_LOST",category="error")
        return redirect("/signup")


    if request.method == "POST":
        input_name = request.form.get('name')
        input_gender = request.form.get('gender')
        input_language = request.form.get('language')
        input_city = request.form.get('city')
        flag_empty = user_control.is_empty(input_name, input_gender,
                                           input_language, input_city)
        
        if flag_empty:
            return render_template("/signup/create-profile.html",labels=labels)
        
        user_info = user.User()
        user_info.id = session['user_id_temp']
        user_info.email = session['user_email_temp']
        user_info.password = session['user_password_temp']
        user_info.country = session['user_country_temp']
        user_info.name = input_name
        user_info.gender = input_gender
        user_info.language = input_language
        user_info.city = input_city
        user_info.websocket_id = session['user_websocket_id_temp']
        
        flag = False
        if flag :
        #if not user_control.push_user_info_to_db(user_info) :
            flash("ERR_CODE:FAILED_TO_PUSH_DB",category="error")
            print("messaged")
        else:
            flash("SUC_CODE:SIGNUP_SUCCEEDS",category="success")

        session.pop('user_id_temp',None)
        session.pop('user_email_temp',None)
        session.pop('user_password_temp',None)
        session.pop('user_country_temp',None)
        session.pop('user_websocket_id_temp', None)

        return redirect("/login")
    else:
        return render_template("/signup/create-profile.html",labels=labels)