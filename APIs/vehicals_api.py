from db import chart_data
from flask import Blueprint, request
from flask_cors import cross_origin
from Models.ModelsAPI import ModelsAPI


vehicales_api = Blueprint('vehicales_api', __name__)

@vehicales_api.route('/vehicalsData', methods=['GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def get_vehicalsData():
    
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    vehicle = request.args.get('vehicle')
    traffic_volume = request.args.get('traffic_volume')
    return {"type":vehicle, "traffic_volume":traffic_volume}
