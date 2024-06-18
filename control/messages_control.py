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

def count_unread_messages(user_id,thread_id=None):
    con = db.DataBase()
    result = 0
    if thread_id==None:
        sql = "SELECT COUNT(*) FROM Messages WHERE recipient_id = '{0}' AND `read` = false"
        result = con.execute_select_one(sql.format(user_id))
    else:
        sql = "SELECT COUNT(*) FROM Messages WHERE recipient_id = '{0}' AND thread_id = '{1}' AND `read` = false"
        result = con.execute_select_one(sql.format(user_id,thread_id))
    
    if not result :
        return 0
    else:
        return int(result['COUNT(*)'])

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
    
def get_chat_room_list(user_id):
    con = db.DataBase()
    query1 = "SELECT * FROM Message_thread WHERE user1_id = '%s' OR user2_id = '%s'"
    query2 = "SELECT * FROM Messages WHERE thread_id = '%s' ORDER BY timestamp DESC"
    results = con.execute_select_all(query1 % (user_id, user_id))
    chat_rooms = []
    for i in results:
        result = con.execute_select_one(query2 % i['thread_id'])
        unread_messages = count_unread_messages(user_id,i['thread_id'])
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
            'recipient_name' : recipient_name,
            'unread_messages' : unread_messages
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
    query = "SELECT * FROM Message_thread WHERE (user1_id = '{0}' AND user2_id = '{1}')\
    OR (user1_id = '{1}' AND user2_id = '{0}')".format(user1_id, user2_id)
    result = con.execute_select_one(query)
    print(result)
    
    if result:
        return result['thread_id']
    else:
        return __make_new_thread(user1_id, user2_id)

def is_in_thread(thread_id,user_id):
    con = db.DataBase()
    query = "SELECT * FROM Message_thread WHERE thread_id = '%s' \
        and (user1_id = '%s' or user2_id = '%s')" % (thread_id,user_id,user_id)
    result = con.execute_select_one(query)
    return result != None

def mark_messages_as_read(user_id,thread_id):
    con = db.DataBase()
    sql = "UPDATE Messages SET `read` = true WHERE recipient_id = '{0}' AND thread_id = '{1}'"
    result, e = con.execute_with_commit(sql.format(user_id,thread_id))

    if not result : print(e)

    return result