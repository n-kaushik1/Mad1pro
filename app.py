from flask import Flask
from backend.models import *
app=None #intially

def init_app():
     mad_app=Flask(__name__) #object of Flask
     mad_app.debug=True
     mad_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///madproject.sqlite3"
     mad_app.app_context().push()  #Direct app access
     db.init_app(mad_app)
     print("Application is started")
     return mad_app

app=init_app()
from backend.controllers import *

if __name__=="__main__":
     app.run()

