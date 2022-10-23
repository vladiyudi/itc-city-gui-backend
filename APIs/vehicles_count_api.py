from flask import Blueprint, request
from flask_cors import cross_origin
import random

vehicles_count_api = Blueprint('vehicles_count_api', __name__)

@vehicles_count_api.route('/vehiclesCount', methods=['GET'])
def vehicles_count():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    all = request.args.get('all')
    print(start_date, end_date, all)
    return {"data":{
   "cars": random.randint(0, 100),
   "busses": random.randint(0, 100),
   "trucks": random.randint(0, 100),
   "pedestrans": random.randint(0, 100),
}}   