from flask import Blueprint
import random
from Models.ModelsAPI import ModelsAPI

vehicles_realtime_api = Blueprint('vehicles_realtime_api', __name__)

@vehicles_realtime_api.route('/realTime_vehicles', methods=['GET'])
def realTime_vehicles():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    return {"cars":random.randint(1,100), "trucks":random.randint(1,100), "buses":random.randint(1,100), "pedestrians":random.randint(1,100)}