from auth import db, USER
import json
import os
import requests
from flask_bcrypt import Bcrypt

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
        user_exists = self.USER.query.filter_by(email=email).first() is not None
        if user_exists:
            return False
        else:
            hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = self.USER(email=email, username=username, password=hashed_password)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        
    
    def send_slack_message(self, user, message):
        slack_message = {'text': f'User {user} has requsted new settings {json.dumps(message)}'}
        requests.post(self.slack, data=json.dumps(slack_message), headers={'Content-Type': 'application/json'})
    
     
        


