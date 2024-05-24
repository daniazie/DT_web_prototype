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

@app.route("/my-profile")
def login():
    return render_template("my-profile.html")