from db import chart_data
from flask import Blueprint
from flask_cors import cross_origin

traffic_volume_api = Blueprint('traffic_volume_api', __name__)

@traffic_volume_api.route('/traffic-volume', methods=['GET'])
@cross_origin(origins="*")
def traffic_volume():
    return {"data":chart_data}