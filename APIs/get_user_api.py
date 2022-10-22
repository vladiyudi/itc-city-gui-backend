from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER

get_user_api = Blueprint('get_user_api', __name__)

@get_user_api.route('/getuser', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def get_user():
    session_data = session.get('user_id')
    user_id = session_data
  
    if not user_id:
        return jsonify({"message": "You are not logged in"}), 401
    
    user = USER.query.filter_by(id=user_id).first()
    return jsonify({"id":user.id, "email":user.email, "username":user.username}), 200
