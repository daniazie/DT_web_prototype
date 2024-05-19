from flask_login import UserMixin
import modules.database as db

class User(UserMixin): 
    def set_info_from_database_by_id(self, user_id):
        connection = db.DataBase()
        result = connection.execute("SELECT * FROM User WHERE id='{0}'".format(user_id))
        connection.__del__()
        if result: 
            self.id = result['id']
            self.password = result['password']
            self.name = result['name']
            return True
        else: # failed to search id from database
            return False

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    
    def check_password(self, password):
        return self.password == password