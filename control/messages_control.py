import models.messages as messages
import models.user as user
import models.database as db
import random, string
import datetime

def __randstrurl():
    con = db.DataBase()
    letters = string.ascii_lowercase
    randstr = ''.join(random.choice(letters) for _ in range(8))
    if not con.execute_select_one("SELECT * FROM messages WHERE thread_id = '%s'" % randstr):
        return randstr
    else:
        return __randstrurl()

def __convert_dict_to_messages(dict):
    data = messages.Messages()
    data.msg_id = dict['msg_id']
    data.sender_id = dict['sender_id']
    data.recipient_id = dict['recipient_id']
    data.message = dict['message']
    data.timestamp = dict['timestamp']
    data.thread_id = dict['thread_id']
    return data

def __make_new_thread(user1_id, user2_id):
    thread_id = __randstrurl()
    con = db.DataBase()
    sql = "INSERT INTO Message_thread (thread_id, user1_id, user2_id) VALUES ('%s', '%s', '%s')"
    values = (thread_id, user1_id, user2_id)
    con.execute_with_commit(sql % values)
    con.execute_with_commit("UPDATE Message_thread mt\
        JOIN User u1 ON mt.user1_id = u1.id JOIN User u2 ON mt.user2_id = u2.id\
        SET	mt.user1_name = u1.name,mt.user2_name = u2.name")

    return thread_id

def push_messages_to_db(data):
    con = db.DataBase()
    sql = "INSERT INTO Messages (sender_id, recipient_id, message, thread_id) VALUES ('%s', '%s', '%s', '%s')"
    values = (data.sender_id, data.recipient_id, data.message, data.thread_id)
    result, _ = con.execute_with_commit(sql % values)
    return result

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    sql = "SELECT * FROM Messages WHERE thread_id = %s ORDER BY timestamp ASC"
    result = con.execute_select_all(sql % thread_id)
    if result:
        return [__convert_dict_to_messages(row) for row in result]
    else:
        return None

def mark_thread_as_read(thread_id, user_id):
    con = db.DataBase()
    sql = "UPDATE Messages SET read = TRUE WHERE thread_id = '%s' AND recipient_id = '%s'"
    con.execute_with_commit(sql % (thread_id, user_id))
    
def get_chat_room_list(user_id):
    con = db.DataBase()
    query1 = "SELECT * FROM Message_thread WHERE user1_id = '%s' OR user2_id = '%s'"
    query2 = "SELECT * FROM Messages WHERE thread_id = '%s' ORDER BY timestamp DESC"
    results = con.execute_select_all(query1 % (user_id, user_id))
    chat_rooms = []
    for i in results:
        result = con.execute_select_one(query2 % i['thread_id'])
        recipient_id = "Unknown"
        recipient_name = "Unknown"

        if i['user1_id'] != user_id:
            recipient_id = i['user1_id']
            recipient_name = i['user1_name']
        else:
            recipient_id = i['user2_id']
            recipient_name = i['user2_name']

        if result == None:
            result = { 'message' : "", 'timestamp' : "" }

        room = {
            'thread_id' : i['thread_id'],
            'last_message' : result['message'],
            'timestamp' : result['timestamp'],
            'recipient_id' : recipient_id,
            'recipient_name' : recipient_name
         }
        chat_rooms.append(room)

    return chat_rooms

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    query = "SELECT * FROM Messages WHERE thread_id = '%s'"
    results = con.execute_select_all(query % (thread_id))
    chat_messages = [__convert_dict_to_messages(row) for row in results]
    return chat_messages

def get_recipient_id_and_name(thread_id, user_id):
    con = db.DataBase()
    query = "SELECT * FROM Message_thread WHERE thread_id = '%s' \
        and (user1_id = '%s' or user2_id = '%s')" % (thread_id,user_id,user_id)
    result = con.execute_select_one(query)
    if result['user1_id'] != user_id:
        return result['user1_id'], result['user1_name']
    else:
        return result['user2_id'], result['user2_name']

def get_timestamp(thread_id, message):
    con = db.DataBase()
    query = "SELECT * FROM Messages WHERE thread_id = '%s' and message = '%s'\
        ORDER BY timestamp DESC" % (thread_id, message)
    result = con.execute_select_one(query)
    return result['timestamp']

def get_thread_id(user1_id, user2_id):
    con = db.DataBase()
    query = "SELECT * FROM Message_thread WHERE user1_id = '%s'" % (user1_id)
    result = con.execute_select_all(query)
    
    for i in result:
        if i['user2_id'] == user2_id:
            return i['thread_id']
        
    thread_id = __make_new_thread(user1_id, user2_id)
    return thread_id

def is_in_thread(thread_id,user_id):
    con = db.DataBase()
    query = "SELECT * FROM Message_thread WHERE thread_id = '%s' \
        and (user1_id = '%s' or user2_id = '%s')" % (thread_id,user_id,user_id)
    result = con.execute_select_one(query)
    return result != None

get_chat_room_list("test01")
import models.messages as messages
import models.user as user
import models.database as db
import datetime

def __convert_dict_to_messages(dict):
    data = messages.Messages()
    data.msg_id = dict['msg_id']
    data.sender_id = dict['sender_id']
    data.recipient_id = dict['recipient_id']
    data.message = dict['message']
    data.timestamp = dict['timestamp']
    data.thread_id = dict['thread_id']
    return data

def push_messages_to_db(data):
    con = db.DataBase()
    sql = "INSERT INTO Messages (msg_id, sender_id, recipient_id, message, timestamp, thread_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data.msg_id, data.sender_id, data.recipient_id, data.message, data.timestamp, data.thread_id)
    result = con.execute_with_commit(sql, values)
    return result

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    sql = "SELECT * FROM Messages WHERE thread_id = %s ORDER BY timestamp ASC"
    result = con.execute_select_all(sql, (thread_id,))
    if result:
        return [__convert_dict_to_messages(row) for row in result]
    else:
        return None

def mark_thread_as_read(thread_id, user_id):
    con = db.DataBase()
    sql = "UPDATE Messages SET read = TRUE WHERE thread_id = %s AND recipient_id = %s"
    con.execute_with_commit(sql, (thread_id, user_id))
    
def get_user_chat_threads(user_id):
    con = db.DataBase()
    query = """
    SELECT thread_id, sender_id, message, timestamp 
    FROM Messages 
    WHERE sender_id = %s
    """
    results = con.execute_select(query, (user_id,))
    chat_threads = [messages.Messages(**row) for row in results]
    return chat_threads

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    query = "SELECT * FROM Messages WHERE thread_id = %s ORDER BY timestamp"
    results = con.execute_select(query, (thread_id,))
    chat_messages = [messages.Messages(**row) for row in results]
    return chat_messages

def get_chat_recipient_name(id):
    con = db.DataBase()
    query = """
    SELECT name
    FROM User 
    WHERE id != %s
    """
    result = con.execute_select_one(query, (id,))
    return result['name'] if result else "Unknown"
