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
    flagged_influencers = Influencer_Info.query.filter_by(flagged="YES").all()
    flagged_sponsors = Sponsor_Info.query.filter_by(flagged="YES").all()
    flagged_list = {f"campaign_{campaign.id}": ["campaign", campaign.name, campaign.sponsor_info.user_name] for campaign in flagged_campaigns}
    flagged_list.update({f"influencer_{influencer.id}": ["influencer", influencer.user_name, influencer.platform] for influencer in flagged_influencers})
    flagged_list.update({f"sponsor_{sponsor.id}": ["sponsor", sponsor.user_name, sponsor.industry] for sponsor in flagged_sponsors})
    return render_template("admindashboard.html", user=uname, campaigns=campaigns, flagged=flagged_list)

@app.route("/adminsearch", methods=["GET", "POST"])
def adminsearch():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    Notflagged_influencers = Influencer_Info.query.filter_by(flagged="NO").all()
    Notflagged_sponsors = Sponsor_Info.query.filter_by(flagged="NO").all()
    Active_list = {f"campaign_{campaign.id}": ["campaign", campaign.name, campaign.sponsor_info.user_name] for campaign in Notflagged_campaigns}
    Active_list.update({f"influencer_{influencer.id}": ["influencer", influencer.user_name, influencer.platform] for influencer in Notflagged_influencers})
    Active_list.update({f"sponsor_{sponsor.id}": ["sponsor", sponsor.user_name, sponsor.industry] for sponsor in Notflagged_sponsors})
    return render_template("adminsearch.html", List=Active_list)



@app.route("/userlogin",methods=["GET","POST"])
def userlogin():
      if request.method=="POST":
        uname=request.form.get("uname")
        pwd=request.form.get("pwd")
        usr1=Influencer_Info.query.filter_by(user_name=uname,password=pwd).first()
        usr2=Sponsor_Info.query.filter_by(user_name=uname,password=pwd).first()
        if usr1:
            session['influencer'] = uname
            return redirect(url_for('influencerdashboard')) 
        elif usr2:
            session['sponsor'] = uname
            return redirect(url_for('sponsordashboard')) 
        else:
            return render_template("userlogin.html",msg="Invalid credentials!!")
      return render_template("userlogin.html")

@app.route("/sponsordashboard", methods=["GET", "POST"])
def sponsordashboard():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    uname = session.get('sponsor')
    campaigns = fetch_campaigns()
    return render_template("sponsordashboard.html",campaigns=campaigns,user=uname)

@app.route("/sponsorsearch", methods=["GET", "POST"])
def sponsorsearch():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    Notflagged_influencers = Influencer_Info.query.filter_by(flagged="NO").all()
    Active_list = {f"campaign_{campaign.id}": ["campaign", campaign.name, campaign.sponsor_info.user_name] for campaign in Notflagged_campaigns}
    Active_list.update({f"influencer_{influencer.id}": ["influencer", influencer.user_name, influencer.platform] for influencer in Notflagged_influencers})
    return render_template("sponsorsearch.html", List=Active_list)

@app.route("/influencerdashboard", methods=["GET", "POST"])
def influencerdashboard():
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))
    uname = session.get('influencer')
    campaigns = fetch_campaigns()
    return render_template("influencerdashboard.html",campaigns=campaigns,user=uname)

@app.route("/influencersearch", methods=["GET", "POST"])
def influencersearch():
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    Notflagged_sponsors = Sponsor_Info.query.filter_by(flagged="NO").all()
    Active_list = {f"campaign_{campaign.id}": ["campaign", campaign.name, campaign.sponsor_info.user_name] for campaign in Notflagged_campaigns}
    Active_list.update({f"sponsor_{sponsor.id}": ["sponsor", sponsor.user_name, sponsor.industry] for sponsor in Notflagged_sponsors})
    return render_template("influencersearch.html", List=Active_list)

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

@app.route("/Influencerregistration",methods=["GET","POST"])
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

 #fetching data   

def fetch_campaigns():
    campaigns=Campaign_Info.query.filter_by(flagged="NO").all()
    campaign_list={}
    for campaign in campaigns:
        progress = calculate_progress(campaign.start_date, campaign.end_date)
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [campaign.name, f"Progress {progress}%",campaign.description]
    return campaign_list

# def fetch_influencers():
#     influencers=Influencer_Info.query.filter_by(flagged="NO").all()
#     influencer_list={}
#     for influencer in influencers:
#         if influencer.id not in influencer_list.keys():
#             influencer_list[influencer.id] = [influencer.user_name,influencer.platform]
#     return influencer_list

# def fetch_sponsors():
#     sponsors=Sponsor_Info.query.filter_by(flagged="NO").all()
#     sponsor_list={}
#     for sponsor in sponsors:
#         if sponsor.id not in sponsor_list.keys():
#             sponsor_list[sponsor.id] = [sponsor.user_name,sponsor.industry]
#     return sponsor_list


        



