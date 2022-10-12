from concurrent.futures import thread
from distutils.log import debug
from socket import socket
from time import sleep
from flask import Flask, render_template
from flask_socketio import SocketIO
import random
from threading import Timer, Thread
import redis
import trafficmonitoring_pb2 as tm
import asyncio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

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
                  movement.append({'posx': x/4, 'posy': y/4})
               socketio.emit('redis data', movement)   
run = True
def stream():
    while run:
      sleep(3) 
      socketio.emit('frontend response', {"data":{
   "cars": random.randint(0, 100),
   "busses": random.randint(0, 100),
   "trucks": random.randint(0, 100),
   "pedestrans": random.randint(0, 100),
}})

# vehicle_data = {
#    "cars": random.randint(0, 100),
#    "busses": random.randint(0, 100),
#    "trucks": random.randint(0, 100),
#    "pedestrans": random.randint(0, 100),
# }
  

@app.route('/')
def index():
   socketio.emit('my event', {'data': 'Connected data'})
   return "Hello man"

# @socketio.on('connect')
# def test_connect():
#    socketio.emit('my response', {'data': 'Connected man'})

   
@socketio.on('new connection')
def handle_my_custom_event(json):
   print('received json: ' + str(json))
   # socketio.emit('redis data', {"data": 'objects'})
   stream()
   # socketio.emit('frontend response', {'data': vehicle_data})

if __name__ == '__main__':
   thread = Thread(target=redis_stream)
   thread.start()
   socketio.run(app, debug=True)