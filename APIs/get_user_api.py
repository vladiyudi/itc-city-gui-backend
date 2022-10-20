from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER

get_user_api = Blueprint('get_user_api', __name__)

@get_user_api.route('/get-user', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*")
def get_user():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User not logged in"}), 401
    
    user = USER.query.filter_by(id=user_id).first()
    return jsonify({"id":user.id, "email":user.email, "username":user.username})