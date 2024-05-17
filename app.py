from flask import Flask, request, url_for, redirect, session, render_template
from flask_login import login_user, LoginManager

import modules.database as db
import modules.user as user

app = Flask(__name__)
app.secret_key = '1q2w3e4r!'

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def hello_world():
    return redirect("/login")

def asdf():
    pass

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    user_id = request.form.get('userID')
    user_pw = request.form.get('userPW')
    print(user_id, user_pw)

    if user_id is None or user_pw is None:
        return render_template('test_login.html')

    connection = db.DataBase()
    sql = "SELECT * FROM User WHERE id='{0}'".format(user_id)
    print(sql)
    user_info = connection.execute(sql)
    connection.__del__()
    print(user_info)
    if user_info == None :
        return render_template('test_login.html')
    elif user_info['password'] == user_pw:
        login_info = user.User(user_info)
        login_user(login_info)
        return redirect('/index')
    else:
        return render_template('test_login.html')

@login_manager.user_loader
def user_loader(user_id):
    connection = db.DataBase()
    user_info = connection.execute("SELECT * FROM User WHERE id='{0}'".format(user_id))
    connection.__del__()
    login_info = user.User(user_info)

    return login_info

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/")

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   