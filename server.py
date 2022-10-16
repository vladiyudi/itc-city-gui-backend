from concurrent.futures import thread
from distutils.log import debug
from socket import socket
from time import sleep
from urllib import request
from wsgiref import headers
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import random
from threading import Timer, Thread, Lock
import redis
import trafficmonitoring_pb2 as tm
from flask_cors import CORS, cross_origin
from markupsafe import escape
from db import chart_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'application/json'
app.config['CORS_ORIGINS'] = ['*']
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

r = redis.Redis('10.10.10.177', 6379)

def redis_stream():
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
                
               socketio.emit('redis data', movement)   
run = True
def stream():
   #  while run:
   #    sleep(5)
      socketio.emit('frontend response', {"data":{
   "cars": random.randint(0, 100),
   "busses": random.randint(0, 100),
   "trucks": random.randint(0, 100),
   "pedestrans": random.randint(0, 100),
}})

def stream2():
    while run:
      sleep(3) 
      socketio.emit('chart data', {"data":{
   {"phase1": random.randint(0, 60), "icon": 'phase1'},
   {"phase2": random.randint(0, 60), "icon": 'phase2'},
   {"phase3": random.randint(0, 60), "icon": 'phase3'},
   {"phase4": random.randint(0, 60), "icon": 'phase4'},
   {"phase5": random.randint(0, 60), "icon": 'phase5'},
   {"phase6": random.randint(0, 60), "icon": 'phase6'},

}})

@app.route('/traffic-volume', methods=['GET'])
@cross_origin(origins="*")
def traffic_volume():
   print('traffic-volume')
   return {"data":chart_data}

@app.route('/')
def index():
   socketio.emit('my event', {'data': 'Connected data'})
   return "Connected"
   
@socketio.on('new connection')
def handle_my_custom_event(json):
   print('received: ' + str(json))
   stream()

@socketio.on('Build chart')
def emitchart(json):
   print('received json: ' + str(json))
   stream2()   

if __name__ == '__main__':
   thread = Thread(target=redis_stream)
   thread.start()
   # redis_stream()
   socketio.run(app, debug=True)