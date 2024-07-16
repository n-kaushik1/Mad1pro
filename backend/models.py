from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy() #Instance of SQLAlchemy

class Influencer_Info(db.Model):
    __tablename__="influencer_info"
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    platform=db.Column(db.String,nullable=False)
    Followers=db.Column(db.Integer,nullable=False)
    

class Sponsor_Info(db.Model):
      __tablename__="sponsor_info"
      id=db.Column(db.Integer,primary_key=True)
      user_name=db.Column(db.String,unique=True,nullable=False)
      password=db.Column(db.String,nullable=False)
      industry=db.Column(db.String,nullable=False)

class Admin_Info(db.Model):
    __tablename__="admin_info"
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
   
     




