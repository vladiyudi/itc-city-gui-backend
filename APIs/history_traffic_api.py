from flask import Blueprint, request
from Views.Pandas import Pandas
from db import chart_data

history_traffic_api = Blueprint('history_traffic_api', __name__)

@history_traffic_api.route('/history-traffic', methods=['GET'])
def history_traffic():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    allDays = request.args.get('allDays')
    chart_data = {"all": 0, "car": 0, "bus": 0, "truck": 0, "peds": 0}
    # car = request.args.get('cars')
    # bus = request.args.get('bus')
    # truck = request.args.get('trucks')
    # print(start_date, end_date)
    # chart = Pandas().build_history_chart("all", start_date, end_date)
    # print (chart)
    
    # chart_data['all'] = Pandas().build_multipledays_chart(start_date, end_date, 'all')  
    # chart_data['car'] = Pandas().build_multipledays_chart(start_date, end_date, 'car') 
    # chart_data['truck'] = Pandas().build_multipledays_chart(start_date, end_date, 'truck') 
    # chart_data['all'] = Pandas().build_multipledays_chart(start_date, end_date, 'van') 
    # chart_data['all'] = Pandas().build_multipledays_chart(start_date, end_date, 'motorbike') 
    
    chart_data = Pandas().build_multipledays_chart(start_date, end_date, 'all') 
        
    return chart_data