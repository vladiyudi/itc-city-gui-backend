from flask import Blueprint, request
from flask_cors import cross_origin
import random
from Models.ModelsAPI import ModelsAPI
from Views.Pandas import Pandas

vehicles_count_api = Blueprint('vehicles_count_api', __name__)

@vehicles_count_api.route('/vehiclesCount', methods=['GET'])
def vehicles_count():
    
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    
    start_date = str(request.args.get('start_date'))
    end_date = str(request.args.get('end_date'))
    
    if start_date == 'undefined':
       start_date = '00:00:00'
    
    if end_date == 'undefined':   
        end_date = '23:45:00'
    
    vehicals = Pandas().count_vehicles(start_date, end_date)

    return {"data":{
   "cars": vehicals['cars'],
   "busses": vehicals['busses'],
   "trucks": vehicals['trucks'],
   "pedestrians": random.randint(0, 100),
}}   