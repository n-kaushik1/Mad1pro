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
    
    # Fetching campaigns
    campaigns = fetch_campaigns()
    
    # Fetching flagged items
    flagged_campaigns = Campaign_Info.query.filter_by(flagged="YES").all()
    flagged_influencers = Influencer_Info.query.filter_by(flagged="YES").all()
    flagged_sponsors = Sponsor_Info.query.filter_by(flagged="YES").all()
    
    flagged_list = {}
    
    # Formatting flagged campaigns
    for campaign in flagged_campaigns:
        flagged_list[f"campaign_{campaign.id}"] = [
            "campaign", campaign.name, campaign.sponsor_info.user_name, campaign.description,
            campaign.start_date, campaign.end_date, campaign.budget, campaign.visibility, campaign.goals
        ]
    
    # Formatting flagged influencers
    for influencer in flagged_influencers:
        flagged_list[f"influencer_{influencer.id}"] = [
            "influencer", influencer.user_name, influencer.platform, influencer.Followers
        ]
    
    # Formatting flagged sponsors
    for sponsor in flagged_sponsors:
        flagged_list[f"sponsor_{sponsor.id}"] = [
            "sponsor", sponsor.user_name, sponsor.industry
        ]
    
    # Passing data to the template
    return render_template(
        "admindashboard.html",
        user=uname,
        campaigns=campaigns,
        flagged=flagged_list
    )

@app.route('/unflag_item/<item_type>/<int:item_id>', methods=['POST'])
def unflag_item(item_type, item_id):
    if item_type == 'campaign':
        item = Campaign_Info.query.get(item_id)
    elif item_type == 'influencer':
        item = Influencer_Info.query.get(item_id)
    elif item_type == 'sponsor':
        item = Sponsor_Info.query.get(item_id)
    else:
        return redirect(url_for('admindashboard'))  # Invalid item type

    if item:
        item.flagged = 'NO'
        db.session.commit()

    return redirect(url_for('admindashboard'))

@app.route("/flag_item/<string:item_type>/<int:item_id>", methods=["POST"])
def flag_item(item_type, item_id):
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))

    if item_type == "campaign":
        item = Campaign_Info.query.get(item_id)
    elif item_type == "influencer":
        item = Influencer_Info.query.get(item_id)
    elif item_type == "sponsor":
        item = Sponsor_Info.query.get(item_id)
    else:
        return "Invalid item type", 400

    if item:
        item.flagged = "YES"
        db.session.commit()
        return redirect(url_for('adminsearch'))
    return "Item not found", 404

@app.route("/adminsearch", methods=["GET", "POST"])
def adminsearch():
    if 'admin' not in session:
        return redirect(url_for('adminlogin'))
    
    # Fetch not flagged campaigns, influencers, and sponsors
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    Notflagged_influencers = Influencer_Info.query.filter_by(flagged="NO").all()
    Notflagged_sponsors = Sponsor_Info.query.filter_by(flagged="NO").all()
    
    # Create the active list with detailed information
    Active_list = {
        f"campaign_{campaign.id}": [
            "campaign", 
            campaign.name, 
            campaign.sponsor_info.user_name,
            campaign.description,
            campaign.start_date,
            campaign.end_date,
            campaign.budget,
            campaign.visibility,
            campaign.goals
        ] for campaign in Notflagged_campaigns
    }
    
    Active_list.update({
        f"influencer_{influencer.id}": [
            "influencer", 
            influencer.user_name, 
            influencer.platform,
            influencer.Followers,
            influencer.role
        ] for influencer in Notflagged_influencers
    })
    
    Active_list.update({
        f"sponsor_{sponsor.id}": [
            "sponsor", 
            sponsor.user_name, 
            sponsor.industry,
            sponsor.role
        ] for sponsor in Notflagged_sponsors
    })
    
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

#sponsor_page_activity
@app.route("/sponsordashboard")
def sponsordashboard():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    
    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    campaigns = Campaign_Info.query.filter_by(sponsor_id=sponsor.id, flagged="NO").all()
    
    campaign_list = {campaign.id: [
        campaign.name,
        campaign.description,
        campaign.start_date,
        campaign.end_date,
        campaign.budget,
        campaign.visibility,
        campaign.goals
    ] for campaign in campaigns}
    
    ad_requests = Adrequest_Info.query.join(Campaign_Info).filter(
        Campaign_Info.sponsor_id == sponsor.id,
        Adrequest_Info.ad_status_sponsor == 'Pending'
    ).all()

    ad_request_list = [{
        'id': request.id,
        'name': request.name,
        'messages': request.messages,
        'requirements': request.requirements,
        'payment_amount': request.payment_amount,
        'ad_staus_sponsor': request.ad_status_sponsor,
        'campaign_name': Campaign_Info.query.get(request.campaign_id).name,
        'influencer_username': request.influencer_username
    } for request in ad_requests]
    
    return render_template("sponsordashboard.html", campaigns=campaign_list, user=uname, ad_requests=ad_request_list)

@app.route("/accept_request_spon/<int:request_id>", methods=['POST'])
def accept_request_spon(request_id):
    ad_request = Adrequest_Info.query.get_or_404(request_id)
    ad_request.ad_status_sponsor = 'Accepted'
    db.session.commit()
    
    return redirect(url_for('sponsordashboard'))

@app.route("/reject_request_spon/<int:request_id>", methods=['POST'])
def reject_request_spon(request_id):
    ad_request = Adrequest_Info.query.get_or_404(request_id)
    ad_request.ad_status_sponsor = 'Rejected'
    db.session.commit()
    
    return redirect(url_for('sponsordashboard'))


@app.route("/sponsorsearch", methods=["GET", "POST"])
def sponsorsearch():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    uname = session.get('sponsor')

    # Fetching not flagged 
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    Notflagged_influencers = Influencer_Info.query.filter_by(flagged="NO").all()

    # Create the active list with all information
    Active_list = {
        f"campaign_{campaign.id}": [
            "campaign", 
            campaign.name, 
            campaign.sponsor_info.user_name,
            campaign.description,
            campaign.start_date,
            campaign.end_date,
            campaign.budget,
            campaign.visibility,
            campaign.goals
        ] for campaign in Notflagged_campaigns
    }
    
    Active_list.update({
        f"influencer_{influencer.id}": [
            "influencer", 
            influencer.user_name, 
            influencer.platform,
            influencer.Followers,
            influencer.role
        ] for influencer in Notflagged_influencers
    })

    success_message = request.args.get('success_message')
    return render_template("sponsorsearch.html", List=Active_list, user=uname, success_message=success_message, campaigns=Notflagged_campaigns)



@app.route("/send_request", methods=["POST"])
def send_request():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    sponsor_name = session.get('sponsor')
    influencer_username = request.form['influencer_username']
    campaign_id = request.form['campaign_id']
    name = request.form['name']
    messages = request.form['messages']
    requirements = request.form['requirements']
    payment_amount = request.form['payment_amount']

    # Create a new Adrequest_Info entry
    new_request = Adrequest_Info(
        name=name,
        messages=messages,
        requirements=requirements,
        payment_amount=payment_amount,
        campaign_id=campaign_id,
        influencer_username=influencer_username
    )

    db.session.add(new_request)
    db.session.commit()

    success_message = 'Request sent successfully!'
    return redirect(url_for('sponsorsearch', success_message=success_message))



@app.route("/sponsorcampaign", methods=["GET", "POST"])
def sponsorcampaign():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    campaigns = Campaign_Info.query.filter_by(sponsor_id=sponsor.id, flagged="NO").all()
    campaign_list = {campaign.id: [campaign.name, campaign.description, f"{calculate_progress(campaign.start_date, campaign.end_date)}%",campaign.start_date,campaign.end_date,campaign.budget,campaign.goals,campaign.visibility] for campaign in campaigns}
    return render_template("sponsorcampaign.html", campaigns=campaign_list, user=uname)

@app.route("/addcampaign", methods=["POST"])
def addcampaign():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        budget = request.form.get("budget")
        goals = request.form.get("goals")
        visibility = request.form.get("visibility")
        
        if not all([name, description, start_date, end_date, budget, goals, visibility]):
            return render_template("sponsorcampaign.html", user=uname, msg="Please fill all fields")

        new_campaign = Campaign_Info(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            goals=goals,
            sponsor_id=sponsor.id,
            visibility=visibility
        )
        db.session.add(new_campaign)
        db.session.commit()

        return redirect(url_for('sponsorcampaign'))
    
@app.route("/editcampaign/<int:campaign_id>", methods=["POST"])
def editcampaign(campaign_id):
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()

    if request.method == "POST":
        campaign = Campaign_Info.query.get_or_404(campaign_id)

        if campaign.sponsor_id != sponsor.id:
            return "Unauthorized", 403

        campaign.name = request.form.get("name")
        campaign.description = request.form.get("description")
        campaign.start_date = request.form.get("start_date")
        campaign.end_date = request.form.get("end_date")
        campaign.budget = request.form.get("budget")
        campaign.goals = request.form.get("goals")
        campaign.visibility = request.form.get("visibility")

        db.session.commit()

        return redirect(url_for('sponsorcampaign'))    
    
@app.route("/deletecampaign/<int:campaign_id>", methods=["POST"])
def deletecampaign(campaign_id):
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()

    campaign = Campaign_Info.query.filter_by(id=campaign_id, sponsor_id=sponsor.id).first()
    
    if not campaign:
        return "Campaign not found or unauthorized", 404
    
    Adrequest_Info.query.filter_by(campaign_id=campaign.id).delete()
    # Delete the campaign
    db.session.delete(campaign)
    db.session.commit()

    return redirect(url_for('sponsorcampaign'))  # Redirect to a suitable page


@app.route("/adsincampaign/<int:campaign_id>", methods=["GET"])
def adsincampaign(campaign_id):
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))
    
    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    campaign = Campaign_Info.query.filter_by(id=campaign_id, sponsor_id=sponsor.id).first()

    if not campaign:
        return "Unauthorized", 403

    ads = Adrequest_Info.query.filter_by( campaign_id=campaign.id).all()
    ads_list = {ad.id: [ad.name, ad.messages, ad.requirements, ad.payment_amount, ad.influencer_username, ad.status] for ad in ads}

    return render_template("adsincampaign.html", ads=ads_list, user=uname, campaign_id=campaign.id)

@app.route("/addad", methods=["POST"])
def addad():
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    campaign_id = request.form.get("campaign_id")
    campaign = Campaign_Info.query.filter_by(id=campaign_id, sponsor_id=sponsor.id).first()

    if not campaign:
        return "Unauthorized", 403

    # Calculate the total budget of existing ads in the campaign
    existing_ads = Adrequest_Info.query.filter_by(campaign_id=campaign.id).all()
    total_ad_budget = sum(float(ad.payment_amount) for ad in existing_ads)
    new_ad_amount = float(request.form.get("payment_amount"))

    # Check if the new ad will exceed the campaign budget
    if total_ad_budget + new_ad_amount > float(campaign.budget):
        ads_list = {ad.id: [ad.name, ad.messages, ad.requirements, ad.payment_amount, ad.influencer_username, ad.status] for ad in existing_ads}
        return render_template("adsincampaign.html", user=uname, msg="Adding ad of this amount will exceeds campaign budget!!", campaign_id=campaign.id, ads=ads_list)

    name = request.form.get("name")
    messages = request.form.get("messages")
    requirements = request.form.get("requirements")
    payment_amount = request.form.get("payment_amount")
    influencer_username = request.form.get("influencer_username")

    if not all([name, messages, requirements, payment_amount, influencer_username]):
        ads_list = {ad.id: [ad.name, ad.messages, ad.requirements, ad.payment_amount, ad.influencer_username, ad.status] for ad in existing_ads}
        return render_template("adsincampaign.html", user=uname, msg="Please fill all fields", campaign_id=campaign.id, ads=ads_list)

    new_ad = Adrequest_Info(
        name=name,
        messages=messages,
        requirements=requirements,
        payment_amount=payment_amount,
        status="Pending",
        campaign_id=campaign.id,
        influencer_username=influencer_username,
        ad_status_sponsor="Accepted"
    )
    db.session.add(new_ad)
    db.session.commit()

    return redirect(url_for('adsincampaign', campaign_id=campaign.id))


@app.route("/editad/<int:ad_id>", methods=["POST"])
def editad(ad_id):
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()

    ad = Adrequest_Info.query.get_or_404(ad_id)
    campaign = Campaign_Info.query.get(ad.campaign_id)

    if campaign.sponsor_id != sponsor.id:
        return "Unauthorized", 403

    # Calculate the total budget of existing ads in the campaign, excluding the ad being edited
    existing_ads = Adrequest_Info.query.filter_by(campaign_id=campaign.id).all()
    total_ad_budget = sum(float(ad.payment_amount) for ad in existing_ads) - float(ad.payment_amount)
    new_ad_amount = float(request.form.get("payment_amount"))

    # Check if the updated ad budget will exceed the campaign budget
    if total_ad_budget + new_ad_amount > float(campaign.budget):
        return "Total ad budget exceeds campaign budget", 400

    ad.name = request.form.get("name")
    ad.messages = request.form.get("messages")
    ad.requirements = request.form.get("requirements")
    ad.payment_amount = request.form.get("payment_amount")
    ad.influencer_username = request.form.get("influencer_username")

    db.session.commit()

    return redirect(url_for('adsincampaign', campaign_id=campaign.id))

    
@app.route("/deletead/<int:ad_id>", methods=["POST"])
def deletead(ad_id):
    if 'sponsor' not in session:
        return redirect(url_for('userlogin'))

    uname = session.get('sponsor')
    sponsor = Sponsor_Info.query.filter_by(user_name=uname).first()
    ad = Adrequest_Info.query.filter_by(id=ad_id).first()
    
    if not ad:
        return "Ad not found", 404

    campaign = Campaign_Info.query.filter_by(id=ad.campaign_id, sponsor_id=sponsor.id).first()
    
    if not campaign:
        return "Unauthorized", 403

    # Delete the ad
    db.session.delete(ad)
    db.session.commit()

    return redirect(url_for('adsincampaign', campaign_id=ad.campaign_id))


#influencer_page_activity
@app.route("/influencerdashboard", methods=["GET", "POST"])
def influencerdashboard():
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))
    
    uname = session.get('influencer')
    
    # Fetch campaigns that are not flagged and have accepted ad requests for this influencer
    campaigns = Campaign_Info.query.join(Adrequest_Info).filter(
        Campaign_Info.flagged == 'NO',
        Adrequest_Info.influencer_username == uname,
        Adrequest_Info.status == 'Accepted'
    ).all()

    for campaign in campaigns:
        progress = calculate_progress(campaign.start_date, campaign.end_date)

    # Fetch new ad requests for this influencer
    new_requests = Adrequest_Info.query.filter(
        Adrequest_Info.influencer_username == uname,
        Adrequest_Info.status == 'Pending'
    ).all()

    return render_template("influencerdashboard.html", campaigns=campaigns, new_requests=new_requests, user=uname,progress=progress)

@app.route("/accept_request/<int:request_id>", methods=["POST"])
def accept_request(request_id):
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))

    request = Adrequest_Info.query.get(request_id)
    if request:
        request.status = 'Accepted'
        db.session.commit()

    return redirect(url_for('influencerdashboard'))


@app.route("/reject_request/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))

    request = Adrequest_Info.query.get(request_id)
    if request:
        request.status = 'Rejected'
        db.session.commit()

    return redirect(url_for('influencerdashboard'))



@app.route("/influencersearch", methods=["GET", "POST"])
def influencersearch():
    if 'influencer' not in session:
        return redirect(url_for('userlogin'))
    Notflagged_campaigns = Campaign_Info.query.filter_by(flagged="NO",visibility="public").all()
    Active_list = {f"campaign_{campaign.id}": ["campaign", campaign.name, campaign.sponsor_info.user_name] for campaign in Notflagged_campaigns}
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

# def fetch_campaigns():
#     campaigns=Campaign_Info.query.filter_by(flagged="NO").all()
#     campaign_list={}
#     for campaign in campaigns:
#         progress = calculate_progress(campaign.start_date, campaign.end_date)
#         if campaign.id not in campaign_list.keys():
#             campaign_list[campaign.id] = [campaign.name, f"Progress {progress}%",campaign.description,campaign.start_date,campaign.end_date,campaign.budget]
#     return campaign_list

def fetch_campaigns():
    campaigns = Campaign_Info.query.filter_by(flagged="NO").all()
    campaign_list = {}
    for campaign in campaigns:
        progress = calculate_progress(campaign.start_date, campaign.end_date)
        campaign_list[campaign.id] = {
            'name': campaign.name,
            'progress': f"Progress {progress}%",
            'description': campaign.description,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'visibility':campaign.visibility,
            'goals':campaign.goals,
            'sponsor_name':campaign.sponsor_info.user_name
        }
    return campaign_list



def fetch_campaignspublic():
    campaigns = Campaign_Info.query.filter_by(flagged="NO", visibility="public").all()
    campaign_list = {}
    for campaign in campaigns:
        progress = calculate_progress(campaign.start_date, campaign.end_date)
        if campaign.id not in campaign_list.keys():
            campaign_list[campaign.id] = [
                campaign.name,
                campaign.description,
                f"Progress {progress}%",
                campaign.start_date,
                campaign.end_date,
                campaign.budget,
                campaign.visibility,
                campaign.goals
            ]
    return campaign_list

# def fetch_influencers():
#     influencers=Influencer_Info.query.filter_by(flagged="NO").all()
#     influencer_list={}
#     for influencer in influencers:
#             influencer_list[influencer.id] = {
#                 user_name:influencer.user_name,
#                 platform:influencer.platform,
#                 Followers=influencer.platform
#                 }
#     return influencer_list

# def fetch_sponsors():
#     sponsors=Sponsor_Info.query.filter_by(flagged="NO").all()
#     sponsor_list={}
#     for sponsor in sponsors:
#         if sponsor.id not in sponsor_list.keys():
#             sponsor_list[sponsor.id] = [sponsor.user_name,sponsor.industry]
#     return sponsor_list


        



