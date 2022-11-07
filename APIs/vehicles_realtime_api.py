from flask import Blueprint, Response
import random
from Models.ModelsAPI import ModelsAPI
from Views.Live_Stream import Live_Stream
import threading

vehicles_realtime_api = Blueprint('vehicles_realtime_api', __name__)

@vehicles_realtime_api.route('/realTime_vehicles', methods=['GET'])
def realTime_vehicles():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    
    
    Live_Stream().generate_mock_data()
    

    return Response(Live_Stream().generate_live_stream(), mimetype='application/json')
    
    