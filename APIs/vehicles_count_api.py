from flask import Blueprint, request
from flask_cors import cross_origin
import random
from Models.ModelsAPI import ModelsAPI

vehicles_count_api = Blueprint('vehicles_count_api', __name__)

@vehicles_count_api.route('/vehiclesCount', methods=['GET'])
def vehicles_count():
    
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    all = request.args.get('all')

    return {"data":{
   "cars": random.randint(0, 100),
   "busses": random.randint(0, 100),
   "trucks": random.randint(0, 100),
   "pedestrans": random.randint(0, 100),
}}   