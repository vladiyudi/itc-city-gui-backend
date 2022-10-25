from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from Views.ViewApi import ViewAPI


register_api = Blueprint('register_api', __name__)

@register_api.route('/signup', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    new_user = ViewAPI(None).register_user(username, email, password)
    
    if not new_user:
        return jsonify({"message": "User already exists"}), 401
      
    return jsonify({"id":new_user.id, "email":new_user.email, "username":new_user.username})