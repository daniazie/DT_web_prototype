from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create-profile")
def create_profile():
    return render_template("create-profile.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/community-posts")
def community_posts():
    return render_template("community-posts.html")

@app.route("/posts")
def posts():
    return render_template("posts.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/my-profile")
def my_profile():
    return render_template("my-profile.html")

@app.route("/my-profile-edit")
def my_profile_edit():
    return render_template("my-profile-edit.html")
