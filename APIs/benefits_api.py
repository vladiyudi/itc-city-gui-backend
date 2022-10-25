from flask import Blueprint
import random
from Models.ModelsAPI import ModelsAPI

benefits_api = Blueprint('benefits_api', __name__)

@benefits_api.route('/benefits', methods=['GET'])
def benefits():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    return {"hours_saved":random.randint(1,100), "money_saved":random.randint(1,1000), "gas_saved":random.randint(1,100)}