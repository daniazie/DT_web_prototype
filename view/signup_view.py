from flask import Flask, flash, redirect, request, render_template, Blueprint, session
from control import lang_control, user_control
from models import user
from uuid import uuid4

signup_view = Blueprint("signup_view", __name__)

@signup_view.route("/signup", methods = ['GET', 'POST'])
def singup():
    labels = lang_control.load_lang_dict("signup",lang_control.selected_lang)
    if request.method == "POST":
        input_id = request.form.get('id')
        input_email = request.form.get('email')
        input_password = request.form.get('password')
        input_country = request.form.get('country')
        
        def websocket_check():
            websocket_id = uuid4().hex
            if not user_control.websocket_id_exists(websocket_id):
                return websocket_id
            else:
                return websocket_check()
        
        websocket_id = websocket_check()
        flag_empty = user_control.is_empty(input_id, input_email,
                                           input_password, input_country)
        print(input_id, input_email,input_password, input_country)
        print(flag_empty)

        if flag_empty:
            return render_template("signup/signup.html", labels=labels)
        
        if user_control.is_exist_id(input_id):
            flash("ERR_CODE:EXIST_ID", category="error")
            return render_template("signup/signup.html", labels=labels) 
                  
        
        session['user_id_temp'] =  input_id
        session['user_email_temp'] = input_email
        session['user_password_temp'] =  user_control.encode_password(input_password)
        session['user_country_temp'] =  input_country
        session['user_websocket_id_temp'] = websocket_id
        
        return redirect("/create-profile")
    else:
        return render_template("signup/signup.html", labels=labels)