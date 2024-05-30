import base64
import models.user as user
import models.database as db

def check_password(user_info, input):
    encoded = base64.b64encode(input.encode("UTF-8")).decode("UTF-8")
    return user_info.password == encoded

def encode_password(input):
    return base64.b64encode(input.encode("UTF-8")).decode("UTF-8")

def is_exist_id(user_id):
    connection = db.DataBase()
    result = connection.execute_select_one("SELECT * FROM User WHERE id='{0}'".format(user_id))
    if result: return True
    else : return False

def pull_user_info_from_db(user_id):
    connection = db.DataBase()
    data = user.User()
    result = connection.execute_select_one("SELECT * FROM User WHERE id='{0}'".format(user_id))
    if result:
        data = user.User()
        data.id = result['id']
        data.password = result['password']
        data.name = result['name']
        data.email = result['email']
        data.country = result['country']
        data.gender = result['gender']
        data.language = result['language']
        data.city = result['city']
        return data
    else: # failed to search id from database
        return None
    
def push_user_info_to_db(user_info):
    connection = db.DataBase()
    if is_exist_id(user_info.id):
        sql = """UPDATE User SET 
                    password='{1}', 
                    name='{2}', 
                    email='{3}', 
                    country='{4}', 
                    gender='{5}', 
                    language='{6}', 
                    city='{7}' 
                 WHERE id='{0}'""".format(
            user_info.id,
            user_info.password,
            user_info.name,
            user_info.email,
            user_info.country,
            user_info.gender,
            user_info.language,
            user_info.city
        )
    else:
        sql = "INSERT INTO dt.User (id, password, name, email, country, gender, language, city) \
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(
            user_info.id,
            user_info.password,
            user_info.name,
            user_info.email,
            user_info.country,
            user_info.gender,
            user_info.language,
            user_info.city
        )
    result,_ = connection.execute_with_commit(sql)
    return result

def is_empty(*args):
    result = False
    
    for i in args:
        result = result or (i == "") or (i == None)
    
    return result