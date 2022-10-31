from flask import Blueprint, request
from Views.Pandas import Pandas
from db import chart_data

history_traffic_api = Blueprint('history_traffic_api', __name__)

@history_traffic_api.route('/history-traffic', methods=['GET'])
def history_traffic():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    allDays = request.args.get('allDays')
    # car = request.args.get('cars')
    # bus = request.args.get('bus')
    # truck = request.args.get('trucks')
    # print(start_date, end_date)
    # chart = Pandas().build_history_chart("all", start_date, end_date)
    # print (chart)
    
    return {"data":chart_data}