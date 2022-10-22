from concurrent.futures import thread
from distutils.log import debug
from time import sleep
from flask import Flask, session
import trafficmonitoring_pb2 as tm
from flask_cors import CORS, cross_origin
from markupsafe import escape
from APIs.vehicals_api import vehicales_api
from APIs.traffic_volume_api import traffic_volume_api
from APIs.vehicles_count_api import vehicles_count_api
from APIs.bar_chart_api import bar_chart_api
from APIs.redis_stream_api import redis_stream_api
from APIs.register_api import register_api
from APIs.login_api import login_api
from APIs.get_user_api import get_user_api
from dotenv import load_dotenv
import os
from auth import db
import redis
from flask_session import Session
from flask.sessions import SecureCookieSessionInterface

load_dotenv()

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='web/static',
            template_folder='web/templates'
            )

CORS(app, 
   #   resources={
   # r"/*": {"origins": "*"}}, 
   supports_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_ORIGINS'] = ['*']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SAMESITE']="None"
app.config['SESSION_COOKIE_SECURE']=True
app.config.from_object(__name__)

session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)

app.register_blueprint(vehicales_api)  
app.register_blueprint(traffic_volume_api)
app.register_blueprint(vehicles_count_api)
app.register_blueprint(bar_chart_api)
app.register_blueprint(redis_stream_api)
app.register_blueprint(register_api)
app.register_blueprint(login_api)
app.register_blueprint(get_user_api)


server_session=Session(app)

db.init_app(app)
with app.app_context():
      db.create_all()

SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_IP = os.getenv('SERVER_IP')

# @app.after_request
# def cookies(response):
#     same_cookie = session_cookie.dumps(dict(session))
#     response.headers.add("Set-Cookie", f"my-cookie={same_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
#     return response

if __name__ == '__main__':
   app.run(debug=True, host=SERVER_IP,  port=SERVER_PORT)
  

