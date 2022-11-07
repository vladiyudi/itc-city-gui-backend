from flask import Blueprint, Response
import random
from Models.ModelsAPI import ModelsAPI
from Views.Live_Stream import Live_Stream

waiting_roi_api = Blueprint('waiting_roi_api', __name__)

@waiting_roi_api.route('/waiting', methods=['GET'])
def waiting():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    
    
    Live_Stream().generate_mock_waiting()
    
    
    
    return Response(Live_Stream().generate_waiting_stream(), mimetype='application/json')               
    
