from db import chart_data
from flask import Blueprint, request
from flask_cors import cross_origin


vehicales_api = Blueprint('vehicales_api', __name__)

@vehicales_api.route('/vehicalsData', methods=['GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def get_vehicalsData():
    vehicle = request.args.get('vehicle')
    traffic_volume = request.args.get('traffic_volume')
    return {"type":vehicle, "traffic_volume":traffic_volume}
