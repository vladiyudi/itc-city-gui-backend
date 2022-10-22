from flask import Blueprint, request, jsonify, session

logout_api = Blueprint('logout_api', __name__)

@logout_api.route('/logout', methods=['OPTIONS', 'POST', 'GET'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "User logged out"}), 200