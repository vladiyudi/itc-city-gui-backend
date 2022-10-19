from flask import Blueprint
from flask_cors import cross_origin
import random

vehicles_count_api = Blueprint('vehicles_count_api', __name__)

@vehicles_count_api.route('/vehiclesCount', methods=['GET'])
@cross_origin(origins="*")
def vehicles_count():
    return {"data":{
   "cars": random.randint(0, 100),
   "busses": random.randint(0, 100),
   "trucks": random.randint(0, 100),
   "pedestrans": random.randint(0, 100),
}}   