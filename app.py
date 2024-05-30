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

@app.route("/community1")
def community1():
    return render_template("/community/community1.html")

@app.route("/community2")
def community2():
    return render_template("/community/community2.html")

@app.route("/community3")
def community3():
    return render_template("/community/community3.html")

@app.route("/community4")
def community4():
    return render_template("/community/community4.html")

@app.route("/posts")
def posts():
    return render_template("posts.html")

@app.route("/posts1")
def posts1():
    return render_template("/posts/posts1.html")

@app.route("/posts2")
def posts2():
    return render_template("/posts/posts2.html")

@app.route("/posts3")
def posts3():
    return render_template("/posts/posts3.html")

@app.route("/posts4")
def posts4():
    return render_template("/posts/posts4.html")

@app.route("/message")
def message():
    return render_template("message.html")

@app.route("/my-profile")
def my_profile():
    return render_template("my-profile.html")

@app.route("/my-profile-edit")
def my_profile_edit():
    return render_template("my-profile-edit.html")
