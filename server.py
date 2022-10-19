from concurrent.futures import thread
from distutils.log import debug
from time import sleep
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Timer, Thread, Lock
import redis
import trafficmonitoring_pb2 as tm
from flask_cors import CORS, cross_origin
from markupsafe import escape
import json
from APIs.vehicals_api import vehicales_api
from APIs.traffic_volume_api import traffic_volume_api
from APIs.vehicles_count_api import vehicles_count_api
from APIs.bar_chart_api import bar_chart_api

app = Flask(__name__, 
            static_url_path='/static', 
            static_folder='web/static',
            template_folder='web/templates'
            )
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_ORIGINS'] = ['*']
app.config['SECRET_KEY'] = 'secret!'

app.register_blueprint(vehicales_api)  
app.register_blueprint(traffic_volume_api)
app.register_blueprint(vehicles_count_api)
app.register_blueprint(bar_chart_api)

lock = Lock()

r = redis.Redis('10.10.10.177', 6379)

def redis_stream():
   global lock
   channel = r.pubsub()
   channel.subscribe('CellGridMapClose')
   for msg in channel.listen():   
      if msg['type'] == 'message': 
               obj = tm.CellGridMapping()
               obj.ParseFromString(msg['data'])
               objects = obj.objects
               movement = []
               for vehicle in objects:
                  x, y = vehicle.pos.x, vehicle.pos.y
                  movement.append({'posx': x/50, 'posy': y/40})  
               yield json.dumps(movement)
                    
@app.route('/redis-stream')
def redis_data():
   return Response(redis_stream(), mimetype='application/json')      


if __name__ == '__main__':
   thread = Thread(target=redis_stream)
   thread.start()
   app.run(debug=True)
