from flask import Flask, request, url_for, redirect, session, render_template
from flask_login import logout_user
from view import login_view, home_view, signup_view, create_profile_view
from view import posts_view, community_view, message_view, my_profile_view, edit_profile_view
from view import post_detail_view, add_post

from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = '1q2w3e4r!'
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(login_view.login_view)
app.register_blueprint(home_view.home_view)
app.register_blueprint(signup_view.signup_view)
app.register_blueprint(create_profile_view.create_profile_view)
app.register_blueprint(edit_profile_view.edit_profile_view)
app.register_blueprint(posts_view.posts_view)
app.register_blueprint(community_view.community_view)
app.register_blueprint(message_view.message_view)
app.register_blueprint(my_profile_view.my_profile_view)
app.register_blueprint(post_detail_view.post_detail_view)
app.register_blueprint(add_post.add_post_view)

@app.route("/")
def hello_world():
    return redirect("/home")

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/home")

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)
   
