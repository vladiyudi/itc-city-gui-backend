from flask import Blueprint
from flask_cors import cross_origin
import random

bar_chart_api = Blueprint('bar_chart_api', __name__)

@bar_chart_api.route('/barChart', methods=['GET'])
@cross_origin(origins="*")
def bar_chart():
    return {"data":[   
   {"data": random.randint(0, 60), "icon": 'phase1'},
   {"data": random.randint(0, 60), "icon": 'phase2'},
   {"data": random.randint(0, 60), "icon": 'phase3'},
   {"data": random.randint(0, 60), "icon": 'phase4'},
   {"data": random.randint(0, 60), "icon": 'phase5'},
   {"data": random.randint(0, 60), "icon": 'phase6'},]}
