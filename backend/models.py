from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy() #Instance of SQLAlchemy

class Admin_Info(db.Model):
    __tablename__="admin_info"
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)

class Influencer_Info(db.Model):
    __tablename__="influencer_info"
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    platform=db.Column(db.String,nullable=False)
    Followers=db.Column(db.Integer,nullable=False)
    name=db.Column(db.String,nullable=False)
    niche=db.Column(db.String,nullable=False)
    adrequest_info=db.relationship("Adrequest_Info",backref="influencer_info")
    flagged=db.Column(db.String,nullable=False,default="NO")     
 

class Sponsor_Info(db.Model):
      __tablename__="sponsor_info"
      id=db.Column(db.Integer,primary_key=True)
      user_name=db.Column(db.String,unique=True,nullable=False)
      password=db.Column(db.String,nullable=False)
      name=db.Column(db.String,nullable=False)
      industry=db.Column(db.String,nullable=False)
      campaign_info=db.relationship("Campaign_Info",backref="sponsor_info")
      flagged=db.Column(db.String,nullable=False,default="NO")



class Campaign_Info(db.Model):
    __tablename__="campaign_info"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False) 
    start_date=db.Column(db.String,nullable=False) 
    end_date=db.Column(db.String,nullable=False)
    budget=db.Column(db.String,nullable=False)
    visibility=db.Column(db.String,nullable=False,default="private")
    goals=db.Column(db.String,nullable=False)
    niche=db.Column(db.String,nullable=False,default="Not specific")
    sponsor_id=db.Column(db.Integer,db.ForeignKey("sponsor_info.id"),nullable=False)
    adrequest_info=db.relationship("Adrequest_Info",backref="campaign_info")
    flagged=db.Column(db.String,nullable=False,default="NO")     
   
class Adrequest_Info(db.Model):
    __tablename__="adrequest_info"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    messages=db.Column(db.String,nullable=False)
    requirements=db.Column(db.String,nullable=False) 
    payment_amount=db.Column(db.String,nullable=False)
    status=db.Column(db.String,nullable=False,default="Pending")
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign_info.id"),nullable=False)
    influencer_username=db.Column(db.String,db.ForeignKey("influencer_info.user_name"),nullable=False)
    ad_status_sponsor=db.Column(db.String,nullable=False,default="Pending")


     




