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
    start_time = args.get('start_time')+':00'
    end_time = args.get('end_time')+':00'
    
    print(start_time, end_time)
    
    
    directions = {'north_south': False, 'south_north': False, 'east_west': False, 'west_east': False} 
    for key in directions:
        directions[key]=request.args.get(key)   
        
        
    days = {'allDays':'true', 'mondays':'false', 'tuesdays':'false', 'wednesdays':'false', 'thursdays':'false', 'fridays':'false', 'saturdays':'false', 'sundays':'false', 'includeWeekends':'true', 'onlyWeekends':'false'} 
    for key in days:
        days[key]=request.args.get(key)
        
    
    if args['allVehicles'] == 'true':
        chart_data['all'] = Pandas().build_multipledays_chart(start_date, end_date, 'all', directions, days) 
        peiod = Pandas().get_traffic_volume_period(start_date, end_date, start_time, end_time, days, 'all') 
   
    if args['cars'] == 'true':
        chart_data['car'] = Pandas().build_multipledays_chart(start_date, end_date, 'car', directions, days)
        peiod = Pandas().get_traffic_volume_period(start_date, end_date, start_time, end_time, days, 'car') 

    if args['trucks'] == 'true':     
        chart_data['truck'] = Pandas().build_multipledays_chart(start_date, end_date, 'truck', directions, days)
        peiod = Pandas().get_traffic_volume_period(start_date, end_date, start_time, end_time, days, 'truck') 
  
    if args['buses']== 'true':       
        chart_data['bus'] = Pandas().build_multipledays_chart(start_date, end_date, 'bus', directions, days)
        peiod = Pandas().get_traffic_volume_period(start_date, end_date, start_time, end_time, days, 'bus') 
    
    if args['pedestrians'] == 'true':    
        chart_data['peds'] = Pandas().build_multipledays_chart(start_date, end_date, 'person', directions, days)
        peiod = Pandas().get_traffic_volume_period(start_date, end_date, start_time, end_time, days, 'person')
                
            
    return {"chart_data":chart_data, "period": peiod}