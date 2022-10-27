from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from Views.ViewApi import ViewAPI


login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def login():
    email = request.json['email']
    password = request.json['password']   
    user = ViewAPI(None).get_user_by_email(email) 
    if user is None:
        return jsonify({"message": "User does not exist"}), 401
    
    if ViewAPI(None).check_password(password, user):
        session['user_id'] = user.id
        return jsonify({"id":user.id, "email":user.email, "username":user.username}), 200
    else:
        return jsonify({"message": "Wrong password"}), 400
    