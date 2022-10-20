from flask import Blueprint, Response
from flask_cors import cross_origin
import trafficmonitoring_pb2 as tm
import redis 
from threading import Lock
import json
from json import JSONEncoder
import os

redis_stream_api = Blueprint('redis_stream_api', __name__)

@redis_stream_api.route('/redis-stream', methods=['GET'])
def redis_data():
   return Response(redis_stream(), mimetype='application/json') 

REDIS_IP = os.getenv('REDIS_IP')
REDIS_PORT = os.getenv('REDIS_PORT')

r = redis.Redis(REDIS_IP, REDIS_PORT)

lock = Lock()

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
                  movement.append({"posx": round(x/50, 2), "posy": round(y/40, 2)})  
               yield json.dumps(movement)