from flask import Blueprint, Response
from flask_cors import cross_origin
import trafficmonitoring_pb2 as tm
from threading import Lock
from Models.ModelsAPI import ModelsAPI
from Views.ViewApi import ViewAPI

redis_stream_api = Blueprint('redis_stream_api', __name__)

@redis_stream_api.route('/redis-stream', methods=['GET'])
def redis_data():
   user_id = ModelsAPI().velidate_user()
   if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
   
   return Response(ViewAPI.redis_stream(), mimetype='application/json') 
