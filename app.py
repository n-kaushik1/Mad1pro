from flask import Flask

app=None #intially

def init_app():
     mad_app=Flask(__name__) #object of Flask
     mad_app.debug=True
     mad_app.app_context().push()  #Direct app access
     print("Application is started")
     return mad_app

app=init_app()
from backend.controllers import *

if __name__=="__main__":
     app.run()

