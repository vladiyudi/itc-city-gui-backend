from flask import Blueprint, request, jsonify, session
from flask_cors import cross_origin
from auth import db, USER
from Models.ModelsAPI import ModelsAPI
from Views.ViewApi import ViewAPI

get_user_api = Blueprint('get_user_api', __name__)

@get_user_api.route('/getuser', methods=['OPTIONS', 'POST', 'GET'])
@cross_origin(origins="*", supports_credentials=True, headers=['Content-Type', 'Authorization'])
def get_user():
    user_id = ModelsAPI().velidate_user()
    if not user_id:
        return {"message": "You are not logged in or unauthorized"}, 401
    
    user = ViewAPI(user_id).get_user_by_id()
    return jsonify({"id":user.id, "email":user.email, "username":user.username}), 200
