from flask import Flask,render_template,request
from flask import current_app as app
from backend.models import *

# @app.route("/")
# def home():
#     return "<h2>Hello</h2>"

@app.route("/",methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        usr=Admin_Info.query.filter_by(user_name=uname,password=pwd).first()
        if usr:
            return render_template("admindashboard.html")
        else:
            return render_template("adminlogin.html",msg="Invalid credentials!!")
    return render_template("adminlogin.html",msg="")

@app.route("/userlogin",methods=["GET","POST"])
def userlogin():
    return render_template("userlogin.html")

@app.route("/Sponsorregistration",methods=["GET","POST"])
def Sponsorregistration():
    return render_template("Sponsorregistration.html")

@app.route("/Influencerrregistration")
def Influencerrregistration():
    return render_template("Influencerregistration.html")


@app.route("/adminsearch")
def user_login():
    return render_template("adminsearch.html")

