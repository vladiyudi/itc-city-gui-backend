from flask import Blueprint
import random

benefits_api = Blueprint('benefits_api', __name__)

@benefits_api.route('/benefits', methods=['GET'])
def benefits():
    return {"hours_saved":random.randint(1,100), "money_saved":random.randint(1,1000), "gas_saved":random.randint(1,100)}