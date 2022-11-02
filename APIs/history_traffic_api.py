from flask import Blueprint, request
from Views.Pandas import Pandas
from db import chart_data

history_traffic_api = Blueprint('history_traffic_api', __name__)

@history_traffic_api.route('/history-traffic', methods=['GET'])
def history_traffic():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    chart_data = {"all": 0, "car": 0, "bus": 0, "truck": 0, "peds": 0}
    args = request.args
    
    
    # day = Pandas().get_days()
    # print(day)
    
    zero = Pandas().build_zero_history_chart(start_date, end_date)
    
    if args['allVehicles'] == 'true':
        chart_data['all'] = Pandas().build_multipledays_chart(start_date, end_date, 'all') 
    else: 
        chart_data['all'] = zero    
    if args['cars'] == 'true':
        chart_data['car'] = Pandas().build_multipledays_chart(start_date, end_date, 'car')
    else:
        chart_data['car'] = zero  
    if args['trucks'] == 'true':     
        chart_data['truck'] = Pandas().build_multipledays_chart(start_date, end_date, 'truck')
    else:
        chart_data['truck'] = zero
    if args['buses']== 'true':       
        chart_data['bus'] = Pandas().build_multipledays_chart(start_date, end_date, 'bus')
    else:
        chart_data['bus'] = zero    
    if args['pedestrians'] == 'true':    
        chart_data['peds'] = Pandas().build_multipledays_chart(start_date, end_date, 'person')
    else:
        chart_data['peds'] = zero   
        
    print(chart_data)     
         
    return chart_data