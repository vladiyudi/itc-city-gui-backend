from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()


login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def login():
    email = request.json['email']
    password = request.json['password']   
    user = USER.query.filter_by(email=email).first()
    
    print(session)
    
    if user is None:
        return jsonify({"message": "User does not exist"}), 401
    
    if bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        print(session)
        return jsonify({"id":user.id, "email":user.email, "username":user.username})
    else:
        return jsonify({"message": "Wrong password"}), 400