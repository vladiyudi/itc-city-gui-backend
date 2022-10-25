from flask import Blueprint, Response
from flask_cors import cross_origin
import trafficmonitoring_pb2 as tm
import redis 
from threading import Lock
import json
import os
from Models.ModelsAPI import ModelsAPI

redis_stream_api = Blueprint('redis_stream_api', __name__)

@redis_stream_api.route('/redis-stream', methods=['GET'])
def redis_data():
   
   # user_id = ModelsAPI().velidate_user()
    
   # if not user_id:
   #      return {"message": "You are not logged in or unathorized"}, 401
   
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
                  movement.append({"x": x, "y": y})  
               yield json.dumps(movement)