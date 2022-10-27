from random import random
from flask import Blueprint
import random
from Models.ModelsAPI import ModelsAPI

itc_efficiency_api = Blueprint('itc_efficiency_api', __name__)


@itc_efficiency_api.route('/itc-efficiency', methods=['GET'])
def itc_efficiency():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    return {"co2": {'itc': random.randint(1, 100), 'no_itc': random.randint(1, 100)}, "travel_time": {'itc': random.randint(1, 100), 'no_itc': random.randint(1, 100)}, "waiting_time": {'itc': random.randint(1, 100), 'no_itc': random.randint(1, 100)}, "fuel_spent": {'itc': random.randint(1, 100), 'no_itc': random.randint(1, 100)}, "time_loss": {'itc': random.randint(1, 100), 'no_itc': random.randint(1, 100)}}
