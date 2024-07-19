from flask import Flask,render_template,request,redirect, url_for, session
from flask import current_app as app
from backend.models import *
from datetime import datetime
import os

app.secret_key = os.urandom(24)



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
            session['admin'] = uname
            return redirect(url_for('admindashboard')) 
        else:
            return render_template("adminlogin.html",msg="Invalid credentials!!")
    return render_template("adminlogin.html",msg="")

@app.route("/admindashboard", methods=["GET", "POST"])
def admindashboard():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))
    uname = session.get('admin')
    campaigns = fetch_campaigns()
    flagged_campaigns = Campaign_Info.query.filter_by(flagged="YES").all()
    flagged_list = {campaign.id: [campaign.name, campaign.sponsor_info.user_name] for campaign in flagged_campaigns}
    return render_template("admindashboard.html", user=uname, campaigns=campaigns, flagged=flagged_list)

# @app.route("/adminsearch")
# def adminsearch():
#     if 'admin' not in session:
#         return redirect(url_for('adminlogin'))
#     return render_template("adminsearch.html")


@app.route("/userlogin",methods=["GET","POST"])
def userlogin():
      if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        usr1=Influencer_Info.query.filter_by(user_name=uname,password=pwd).first()
        usr2=Sponsor_Info.query.filter_by(user_name=uname,password=pwd).first()
        if usr1:
            return render_template("influencerdashboard.html",msg=usr1.user_name)
        elif usr2:
            return render_template("sponsordashboard.html",msg=usr2.user_name)
        else:
            return render_template("userlogin.html",msg="Invalid credentials!!")
      return render_template("userlogin.html")

#registration

@app.route("/Sponsorregistration",methods=["GET","POST"])
def Sponsorregistration():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        ind=request.form.get("ind")
        usr=Sponsor_Info.query.filter_by(user_name=uname).first()
        if not usr:
            new_user=Sponsor_Info(user_name=uname,password=pwd,industry=ind)
            db.session.add(new_user)
            db.session.commit()
            return render_template("userlogin.html")
        else:
            return render_template("Influencerregistration.html",msg="Sorry user already existed!!!")
    return render_template("Sponsorregistration.html")

@app.route("/Influencerrregistration",methods=["GET","POST"])
def Influencerrregistration():
    if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        plat=request.form.get("plat")
        flw=request.form.get("flw")
        usr=Influencer_Info.query.filter_by(user_name=uname).first()
        if not usr:
            new_user=Influencer_Info(user_name=uname,password=pwd,platform=plat,Followers=flw)
            db.session.add(new_user)
            db.session.commit()
            return render_template("userlogin.html")
        else:
            return render_template("Influencerregistration.html",msg="Sorry user already existed!!!")
     
    return render_template("Influencerregistration.html")


   
def calculate_progress(start_date, end_date):
    start = datetime.strptime(start_date, "%d-%m-%y")
    end = datetime.strptime(end_date, "%d-%m-%y")
    now = datetime.now()

    if now < start:
        return 0
    elif now > end:
        return 100
    else:
        total_duration = (end - start).days
        elapsed_duration = (now - start).days
        progress = (elapsed_duration / total_duration) * 100
        return int(progress)  
    
def fetch_campaigns():
    campaigns=Campaign_Info.query.filter_by(flagged="NO").all()
    campaign_list={}
    for campaign in campaigns:
        progress = calculate_progress(campaign.start_date, campaign.end_date)
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, f"Progress {progress}%"]
    return campaign_list


        



