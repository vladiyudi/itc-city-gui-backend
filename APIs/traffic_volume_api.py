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
    bus = request.args.get('bus')
    truck = request.args.get('trucks')
    
    print (all, car, bus)
    
    if start_date == 'undefined':
       start_date = '00:00:00'
    
    if end_date == 'undefined':   
        end_date = '23:45:00'
    
    if all == 'true':
        print ("all")
        chart = Pandas().build_basic_chart(start_date, end_date)
    elif car == 'true':
        chart = Pandas().build_vehicles_chart(start_date, end_date, 'car') 
    elif truck == 'true':
        chart = Pandas().build_vehicles_chart(start_date, end_date, 'truck') 
        
        
    lane = Pandas().get_lanes(start_date, end_date)      

    return {"data":chart, "lanes": lane}