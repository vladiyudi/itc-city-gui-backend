from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER
from flask_bcrypt import Bcrypt



bcrypt = Bcrypt()


login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*")
def login():
    email = request.json['email']
    password = request.json['password']
    
    print(email, password)
    
    user = USER.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"message": "User does not exist"}), 401
    
    if bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({"id":user.id, "email":user.email, "username":user.username})
    else:
        return jsonify({"message": "Wrong password"}), 400