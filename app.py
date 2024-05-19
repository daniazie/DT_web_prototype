from flask import Flask, request, url_for, redirect, session, render_template
from flask_login import login_user, LoginManager

import modules.user as user

app = Flask(__name__)
app.secret_key = '1q2w3e4r!'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def hello_world():
    return redirect("/login")

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    user_id = request.form.get('Username')
    user_pw = request.form.get('Password')
    print(user_id, user_pw)

    if user_id is None or user_pw is None:
        return render_template('login.html')

    user_info = user.User()
    
    flag = user_info.set_info_from_database_by_id(user_id)
    if flag:
        if user_info.check_password(user_pw):
            login_user(user_info)
            return redirect('/index')

    return render_template('login.html')

@login_manager.user_loader
def user_loader(user_id):
    user_info = user.User()
    user_info.set_info_from_database_by_id(user_id)
    return user_info

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   