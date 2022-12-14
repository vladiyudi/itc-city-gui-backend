from concurrent.futures import thread
from distutils.log import debug
from flask import Flask
from flask_cors import CORS
from markupsafe import escape
from APIs.vehicals_api import vehicales_api
from APIs.traffic_volume_api import traffic_volume_api
from APIs.vehicles_count_api import vehicles_count_api
from APIs.bar_chart_api import bar_chart_api
from APIs.redis_stream_api import redis_stream_api
from APIs.register_api import register_api
from APIs.login_api import login_api
from APIs.get_user_api import get_user_api
from APIs.logout_api import logout_api
from APIs.itc_efficiency_api import itc_efficiency_api
from APIs.benefits_api import benefits_api
from APIs.policy_choose_api import policy_choose_api
from APIs.problem_report_api import problem_report_api
from APIs.vehicles_realtime_api import vehicles_realtime_api
from APIs.history_traffic_api import history_traffic_api
from APIs.historical_traffic_count_api import historical_traffic_count_api
from APIs.waiting_roi_api import waiting_roi_api
from dotenv import load_dotenv
import os
from auth import db
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
app.register_blueprint(logout_api)
app.register_blueprint(itc_efficiency_api)
app.register_blueprint(benefits_api)
app.register_blueprint(policy_choose_api)
app.register_blueprint(problem_report_api)
app.register_blueprint(vehicles_realtime_api)
app.register_blueprint(history_traffic_api)
app.register_blueprint(historical_traffic_count_api)
app.register_blueprint(waiting_roi_api)


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
   app.run(debug=True, host="0.0.0.0",  port=SERVER_PORT)
  

