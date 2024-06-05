import models.messages as messages
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
    sql = "INSERT INTO messages (msg_id, sender_id, recipient_id, message, timestamp, thread_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (data.msg_id, data.sender_id, data.recipient_id, data.message, data.timestamp, data.thread_id)
    result = con.execute_with_commit(sql, values)
    return result

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    sql = "SELECT * FROM messages WHERE thread_id = %s ORDER BY timestamp ASC"
    result = con.execute_select_all(sql, (thread_id,))
    if result:
        return [__convert_dict_to_messages(row) for row in result]
    else:
        return None

def mark_thread_as_read(thread_id, user_id):
    con = db.DataBase()
    sql = "UPDATE messages SET read = TRUE WHERE thread_id = %s AND recipient_id = %s"
    con.execute_with_commit(sql, (thread_id, user_id))
    
def get_user_chat_threads(user_id):
    con = db.DataBase()
    query = """
    SELECT thread_id, sender_name, last_message, timestamp 
    FROM chat_threads 
    WHERE user_id = %s
    """
    results = con.execute_select(query, (user_id,))
    chat_threads = [chat(**row) for row in results]
    return chat_threads

def pull_messages_from_db_by_thread(thread_id):
    con = db.DataBase()
    query = "SELECT * FROM messages WHERE thread_id = %s ORDER BY timestamp"
    results = con.execute_select(query, (thread_id,))
    chat_messages = [Message(**row) for row in results]
    return chat_messages

def get_chat_recipient_name(thread_id, user_id):
    con = db.DataBase()
    query = """
    SELECT recipient_name 
    FROM chat_threads 
    WHERE thread_id = %s AND user_id != %s
    """
    result = con.execute_select_one(query, (thread_id, user_id))
    return result['recipient_name'] if result else "Unknown"
