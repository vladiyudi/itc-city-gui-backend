from flask import Blueprint, request
from Models.ModelsAPI import ModelsAPI
from Views.Pandas import Pandas

historical_traffic_count_api = Blueprint('historical_traffic_count_api', __name__)

@historical_traffic_count_api.route('/historicalTrafficCount', methods=['GET'])
def traffic_count():
    
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    
    vehicals = Pandas().count_history_vehicals(start, end)
    
    return {"data":{
   "cars": vehicals['cars'],
   "busses": vehicals['busses'],
   "trucks": vehicals['trucks'],
   "pedestrians": vehicals['pedestrians'],
}}   