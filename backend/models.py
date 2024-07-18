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
    role=db.Column(db.Integer,nullable=False,default=1)
    adrequest_info=db.relationship("Adrequest_Info",backref="influencer_info")     
 

class Sponsor_Info(db.Model):
      __tablename__="sponsor_info"
      id=db.Column(db.Integer,primary_key=True)
      user_name=db.Column(db.String,unique=True,nullable=False)
      password=db.Column(db.String,nullable=False)
      industry=db.Column(db.String,nullable=False)
      role=db.Column(db.Integer,nullable=False,default=2)
      campaign_info=db.relationship("Campaign_Info",backref="sponsor_info")     


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
    sponsor_id=db.Column(db.Integer,db.ForeignKey("sponsor_info.id"),nullable=False)
    adrequest_info=db.relationship("Adrequest_Info",backref="campaign_info")     
   
class Adrequest_Info(db.Model):
    __tablename__="adrequest_info"
    id=db.Column(db.Integer,primary_key=True)
    messages=db.Column(db.String,nullable=False)
    requirements=db.Column(db.String,nullable=False) 
    payment_amount=db.Column(db.String,nullable=False)
    status=db.Column(db.String,nullable=False,default="Pending")
    campaign_id=db.Column(db.Integer,db.ForeignKey("campaign_info.id"),nullable=False)
    influencer_id=db.Column(db.Integer,db.ForeignKey("influencer_info.id"),nullable=False)

     




