from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_info):
        self.id = user_info['id']
        self.password = user_info['password']
        self.name = user_info['name']
        

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name