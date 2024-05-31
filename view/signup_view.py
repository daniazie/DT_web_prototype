from flask import Flask, flash, redirect, request, render_template, Blueprint, session
from control import user_control
from models import user

signup_view = Blueprint("signup_view", __name__)

@signup_view.route("/signup", methods = ['GET', 'POST'])
def singup():
    if request.method == "POST":
        input_id = request.form.get('id')
        input_email = request.form.get('email')
        input_password = request.form.get('password')
        input_country = request.form.get('country')
        flag_empty = user_control.is_empty(input_id, input_email,
                                           input_password, input_country)

        if flag_empty:
            return render_template("signup.html")
        
        if user_control.is_exist_id(input_id):
            flash("an already existing ID", category="error")
            return render_template("signup.html")   
        
        session['user_id_temp'] =  input_id
        session['user_email_temp'] = input_email
        session['user_password_temp'] =  user_control.encode_password(input_password)
        session['user_country_temp'] =  input_country
        
        # id = session['user_id_temp']
        # email = session['user_email_temp']
        # country = session['user_country_temp']
        
        return redirect("/create-profile")
    else:
        return render_template("signup.html")