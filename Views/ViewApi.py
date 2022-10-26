from auth import db, USER
import json
import os
import requests
from flask_bcrypt import Bcrypt
import trafficmonitoring_pb2 as tm
import redis 
from threading import Lock

REDIS_IP = os.getenv('REDIS_IP')
REDIS_PORT = os.getenv('REDIS_PORT')
r = redis.Redis(REDIS_IP, REDIS_PORT)
lock = Lock()

class ViewAPI:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = db
        self.USER = USER
        self.slack = os.getenv('SLACK_WEBHOOK')
        self.bcrypt = Bcrypt()

    def get_user_by_id(self):
        user = self.USER.query.filter_by(id=self.user_id).first()
        return user

    def get_user_by_email(self, email):
        user = self.USER.query.filter_by(email=email).first()
        return user

    def check_password(self, password, user):
        if self.bcrypt.check_password_hash(user.password, password):
            return True
        else:
            return False

    def register_user(self, username, email, password):
        user_exists = self.USER.query.filter_by(
            email=email).first() is not None
        if user_exists:
            return False
        else:
            hashed_password = self.bcrypt.generate_password_hash(
                password).decode('utf-8')
            new_user = self.USER(
                email=email, username=username, password=hashed_password)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user

    def send_slack_message(self, user, message, type):
        if type == "problem_report":
            slack_message = {
                "text": "New problem report",
                "attachments": [
                    {
                        "text": f"User: {user} reported a problem: {message['problem']}"
                    }
                ]
            }
        elif type == "policy_choose":
            slack_message = {
                "text": "New policy choose",
                "attachments": [
                    {'text': f'User {user} has requsted new settings {json.dumps(message)}'}]}
        requests.post(self.slack, data=json.dumps(slack_message),
                      headers={'Content-Type': 'application/json'})


    def redis_stream():
        global lock
        channel = r.pubsub()
        channel.subscribe('CellGridMapClose')
        for msg in channel.listen():   
            if msg['type'] == 'message': 
                    obj = tm.CellGridMapping()
                    obj.ParseFromString(msg['data'])
                    objects = obj.objects
                    movement = []
                    for vehicle in objects:
                        x, y = vehicle.pos.x, vehicle.pos.y
                        movement.append({"x": x, "y": y})  
                    yield json.dumps(movement)     