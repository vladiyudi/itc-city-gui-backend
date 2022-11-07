from flask import Blueprint, Response
import random
from Models.ModelsAPI import ModelsAPI
from Views.Live_Stream import Live_Stream

bar_chart_api = Blueprint('bar_chart_api', __name__)

@bar_chart_api.route('/barChart', methods=['GET'])
def bar_chart():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    
    
    Live_Stream().generate_mock_barChart()
    
    return Response(Live_Stream().generate_barChart_stream(), mimetype='application/json')               
    
    
#     return {"data":[   
#    {"data": random.randint(0, 60), "icon": 'phase1'},
#    {"data": random.randint(0, 60), "icon": 'phase2'},
#    {"data": random.randint(0, 60), "icon": 'phase3'},
#    {"data": random.randint(0, 60), "icon": 'phase4'},
#    {"data": random.randint(0, 60), "icon": 'phase5'},
#    {"data": random.randint(0, 60), "icon": 'phase6'},
#    ]}
