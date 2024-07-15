from flask import Flask,render_template
from flask import current_app as app

# @app.route("/")
# def home():
#     return "<h2>Hello</h2>"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

@app.route("/Sponsorregistration")
def Sponsorregistration():
    return render_template("Sponsorregistration.html")

@app.route("/Influencerrregistration")
def Influencerrregistration():
    return render_template("Influencerregistration.html")

@app.route("/admindashboard")
def admindashboard():
    return render_template("admindashboard.html")

@app.route("/adminsearch")
def user_login():
    return render_template("adminsearch.html")