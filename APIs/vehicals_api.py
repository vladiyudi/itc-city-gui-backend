from db import chart_data
from flask import Blueprint
from flask_cors import cross_origin

vehicales_api = Blueprint('vehicales_api', __name__)

@vehicales_api.route('/vehicalsData/<type>', methods=['GET'])
@cross_origin(origins="*")
def get_vehicalsData(type):
    return {type:chart_data}
