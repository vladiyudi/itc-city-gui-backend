from email import header
from db import chart_data
from flask import Blueprint
from flask_cors import cross_origin
from Models.ModelsAPI import ModelsAPI

traffic_volume_api = Blueprint('traffic_volume_api', __name__)

@traffic_volume_api.route('/traffic-volume', methods=['GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def traffic_volume():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    return {"data":chart_data}