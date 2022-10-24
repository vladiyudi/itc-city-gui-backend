from flask import Blueprint, request, session
from auth import db, USER
import json
import os
import requests

policy_choose_api = Blueprint('policy_choose_api', __name__)

slack = os.getenv('SLACK_WEBHOOK')

@policy_choose_api.route('/policy-choose', methods=['POST'])
def policy_choose():
    user_id = session.get('user_id')
    user = USER.query.filter_by(id=user_id).first()
    data = request.get_json()
    
    slack_message = {'text': f'User {user.username} has chosen policy'}
    
    requests.post(slack, data=json.dumps(slack_message), headers={'Content-Type': 'application/json'})
    
    return {"user": user.username}