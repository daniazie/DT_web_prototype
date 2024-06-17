from flask import Flask, request, redirect, jsonify, render_template, Blueprint
from flask_login import login_required, current_user
from models import messages
from models.socketio import socketio
from control import lang_control, messages_control, user_control
import models.database as db
import random, string
from datetime import datetime

message_view = Blueprint("message_view", __name__)

def randstrurl():
    con = db.DataBase()
    letters = string.ascii_lowercase
    randstr = ''.join(random.choice(letters) for _ in range(8))
    if not con.execute_select_one("SELECT * FROM messages WHERE thread_id = %s" % randstr):
        return randstr
    else:
        return randstrurl()

@message_view.route("/messages")
@login_required
def home():
    labels = lang_control.load_lang_dict("messages",lang_control.selected_lang)
    chat_rooms = messages_control.get_chat_room_list(current_user.id)
    return render_template("message/message.html", chats=chat_rooms, user=current_user,labels=labels)

@message_view.route("/messages/room/redirect")
@login_required
def redirect_chat():
    labels = lang_control.load_lang_dict("messages",lang_control.selected_lang)
    user1_id = request.args.get("uid1")
    user2_id = request.args.get("uid2")
    if user1_id == user2_id:
        return redirect("/messages")

    thread_id = messages_control.get_thread_id(user1_id,user2_id)
    return redirect("/messages/room?id={0}".format(thread_id),labels=labels)

@message_view.route("/messages/room")
@login_required
def view_chat():
    labels = lang_control.load_lang_dict("messages",lang_control.selected_lang)
    # Fetch messages for the specific chat thread
    thread_id = request.args.get("id")
    if not messages_control.is_in_thread(thread_id,current_user.id):
        print("kicked")
        return redirect("/messages")
    
    chat_messages = messages_control.pull_messages_from_db_by_thread(thread_id)
    messages_control.mark_messages_as_read(current_user.id,thread_id)
    chat_recipient_id, chat_recipient_name = messages_control.get_recipient_id_and_name(thread_id, current_user.id)
    return render_template("message/message_detail.html", messages=chat_messages,
                chat_recipient_id=chat_recipient_id, chat_recipient_name=chat_recipient_name,
            user=current_user, thread_id=thread_id,labels=labels)

@socketio.on("send_message")
def send_message(data):
    thread_id = data.get('thread_id')

    message = messages.Messages()
    message.sender_id=current_user.id
    message.recipient_id=data.get('recipient_id')
    message.message=data.get('message')
    message.thread_id=data.get('thread_id')

    timestamp = datetime(1900,1,1,0,0,0)

    if not messages_control.push_messages_to_db(message):
        print("sql failed")
        return jsonify({"error": "Failed to send message"}), 500
    else:
        timestamp = messages_control.get_timestamp(thread_id, message.message)

    socketio.emit(f"{thread_id}_newmsg",
                  {'thread_id': data.get('thread_id'),
                    'message': data.get('message'),
                    'recipient_id' : message.recipient_id,
                    'recipient_name' : data.get('chat_recipient_name'),
                    'sender_name' : current_user.name,
                    'timestamp' : timestamp.strftime('%m/%d %H:%M:%S')
                   })
    socketio.emit(f"shake_newmsg",
                  {'thread_id': data.get('thread_id'),
                    'recipient_id' : message.recipient_id,
                    'sender_id' : message.sender_id
                   })
    return jsonify({"status": "Message sent", "thread_id": thread_id}), 200

@socketio.on("read_message")
def read_message(data):
    thread_id = data.get('thread_id')
    recipient_id = data.get('recipient_id')

    if not messages_control.mark_messages_as_read(recipient_id,thread_id):
        print("sql failed")
        return jsonify({"error": "Failed to mark message as read"}), 500

    return jsonify({"status": "Marked a message as read", 
                    "thread_id": thread_id, 
                    "recipient_id": recipient_id}), 200

@socketio.on("check_unread_message")
def read_message(data):
    recipient_id = data.get('recipient_id')
    socketio.emit(f"check_unread_message_response",
                  {'message_to_read': current_user.message_to_read},to=request.sid)

    return jsonify({"status": "Checked message unread", "recipient_id": recipient_id}), 200

