from flask import Flask, request, url_for, redirect, session, render_template
from flask_login import login_user, LoginManager
from view import login_view

app = Flask(__name__)
app.secret_key = '1q2w3e4r!'

app.register_blueprint(login_view.login_view)

@app.route("/")
def hello_world():
    return redirect("/login")

@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   