from flask import Blueprint, Response
from flask_cors import cross_origin
import trafficmonitoring_pb2 as tm
import redis 
from threading import Lock
import json
from json import JSONEncoder

redis_stream_api = Blueprint('redis_stream_api', __name__)

@redis_stream_api.route('/redis-stream', methods=['GET'])
def redis_data():
   return Response(redis_stream(), mimetype='application/json') 

r = redis.Redis('10.10.10.177', 6379)  

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
                  if x > 0.1 and y > 0.1:
                    movement.append({'posx': round(x/50, 2), 'posy': round(y/40, 2)})  
               yield json.dumps(movement)