from flask import Blueprint, request
from Views.ViewApi import ViewAPI
from Models.ModelsAPI import ModelsAPI

problem_report_api = Blueprint('problem_report_api', __name__)

@problem_report_api.route('/problem-report', methods=['POST'])
def problem_report():
    user_id = ModelsAPI().velidate_user()
    
    if not user_id:
        return {"message": "You are not logged in or unathorized"}, 401
    
    user = ViewAPI(user_id).get_user_by_id()
    ViewAPI(user_id).send_slack_message(user.username, request.json, "problem_report") 
    
    return {"user": user.username}, 200
