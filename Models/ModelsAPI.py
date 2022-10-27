from flask import session

class ModelsAPI:
    def __init__(self):
        self.session = session

    def velidate_user(self):
        user_id = self.session.get('user_id')
        if user_id:
            return user_id
        else:
            return False