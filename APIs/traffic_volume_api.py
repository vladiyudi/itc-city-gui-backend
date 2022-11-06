from email import header
from flask import Blueprint, request
from flask_cors import cross_origin
from Models.ModelsAPI import ModelsAPI
from Views.Pandas import Pandas
from Views.ViewApi import ViewAPI

traffic_volume_api = Blueprint('traffic_volume_api', __name__)

@traffic_volume_api.route('/traffic-volume', methods=['GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def traffic_volume():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    all = request.args.get('all')
    car = request.args.get('cars')
    bus = request.args.get('buses')
    truck = request.args.get('trucks')
    peds = request.args.get('pedestrians')
      
    if start_date == 'undefined':
       start_date = '00:00:00'
    
    if end_date == 'undefined':   
        end_date = '23:45:00'
     
    chart = {"all": 0, "car": 0, "bus": 0, "truck": 0, "peds": 0}  
    zero = Pandas().build_zero_chart(start_date, end_date) 
    
    if all == 'true':
        chart["all"] = Pandas().build_basic_chart(start_date, end_date)
    else: 
        chart["all"] = zero    
    if car == 'true':
        chart["car"] = Pandas().build_vehicles_chart(start_date, end_date, 'car') 
    else:
        chart['car'] = zero   
    if truck == 'true':
        chart["truck"] = Pandas().build_vehicles_chart(start_date, end_date, 'truck') 
    else:
        chart['truck'] = zero   
    if bus == 'true':
        chart["bus"] = Pandas().build_vehicles_chart(start_date, end_date, 'bus')
    else: 
        chart['bus'] = zero    
    if peds == 'true':
        chart["peds"] = Pandas().build_vehicles_chart(start_date, end_date, 'person')
    else: 
        chart['peds'] = zero            
        
    lane = Pandas().get_lanes(start_date, end_date)   
    
    return {"data":chart, "lanes": lane['vehicals'], 'peds': lane['peds']}