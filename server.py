from concurrent.futures import thread
from distutils.log import debug
from time import sleep
from flask import Flask
import trafficmonitoring_pb2 as tm
from flask_cors import CORS, cross_origin
from markupsafe import escape
from APIs.vehicals_api import vehicales_api
from APIs.traffic_volume_api import traffic_volume_api
from APIs.vehicles_count_api import vehicles_count_api
from APIs.bar_chart_api import bar_chart_api
from APIs.redis_stream_api import redis_stream_api
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='web/static',
            template_folder='web/templates'
            )
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_ORIGINS'] = ['*']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(vehicales_api)  
app.register_blueprint(traffic_volume_api)
app.register_blueprint(vehicles_count_api)
app.register_blueprint(bar_chart_api)
app.register_blueprint(redis_stream_api)

SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_IP = os.getenv('SERVER_IP')

if __name__ == '__main__':
   app.run(debug=True, host=SERVER_IP,  port=SERVER_PORT)
