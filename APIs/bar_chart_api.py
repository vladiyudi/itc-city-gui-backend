from flask import Blueprint
from flask_cors import cross_origin
import random
import csv
from Models.ModelsAPI import ModelsAPI

bar_chart_api = Blueprint('bar_chart_api', __name__)

@bar_chart_api.route('/barChart', methods=['GET'])
def bar_chart():
    
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    
    with open('TLVTrafficCounting15-2022-08-22.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        # print (data[0])
    return {"data":[   
   {"data": random.randint(0, 60), "icon": 'phase1'},
   {"data": random.randint(0, 60), "icon": 'phase2'},
   {"data": random.randint(0, 60), "icon": 'phase3'},
   {"data": random.randint(0, 60), "icon": 'phase4'},
   {"data": random.randint(0, 60), "icon": 'phase5'},
   {"data": random.randint(0, 60), "icon": 'phase6'},
   ],  "csv": data}
