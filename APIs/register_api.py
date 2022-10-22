from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

register_api = Blueprint('register_api', __name__)

@register_api.route('/signup', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
      
    user_exists = USER.query.filter_by(email=email).first() is not None
    
    if user_exists:
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')    
    new_user = USER(email=email, username=username, password=hashed_password)
    db.session.add(new_user)  
    db.session.commit()
    
    return jsonify({"id":new_user.id, "email":new_user.email, "username":new_user.username})