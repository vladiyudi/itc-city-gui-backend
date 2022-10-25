from flask import Blueprint, request, session
from Views.ViewApi import ViewAPI
from Models.ModelsAPI import ModelsAPI

policy_choose_api = Blueprint('policy_choose_api', __name__)

@policy_choose_api.route('/policy-choose', methods=['POST'])
def policy_choose():
    
    user_id = ModelsAPI().velidate_user()
    
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    user = ViewAPI(user_id).get_user_by_id()
    ViewAPI(user_id).send_slack_message(user.username, request.json)   
    
    return {"user": user.username}, 200