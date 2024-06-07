from flask import Flask, request, redirect, jsonify, render_template, Blueprint
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
import models.user as user
from models import messages
import control.messages_control as messages_control
import control.user_control as user_control
import models.database as db
import random, string
from datetime import datetime
from uuid import uuid4

message_view = Blueprint("message_view", __name__)
socketio = SocketIO(logger=True, engineio_logger=True)

@message_view.record_once
def on_load(state):
    socketio.init_app(state.app, cors_allowed_origins="*")

def randstrurl():
    con = db.DataBase()
    letters = string.ascii_lowercase
    randstr = ''.join(random.choice(letters) for _ in range(8))
    if not con.execute_select_one("SELECT * FROM messages WHERE thread_id = %s", (randstr,)):
        return randstr
    else:
        return randstrurl()

@message_view.route("/messages")
@login_required
def home():
    # Fetch all chat threads for the current user
    chat_rooms = messages_control.get_chat_room_list(current_user.id)
    print(chat_rooms)
    return render_template("message.html", chats=chat_rooms)

@message_view.route("/messages/room/redirect")
@login_required
def redirect_chat():
    user1_id = request.args.get("uid1")
    user2_id = request.args.get("uid2")
    if user1_id == user2_id:
        return redirect("/messages")

    thread_id = messages_control.get_thread_id(user1_id,user2_id)
    print("/messages/room?id={0}".format(thread_id))
    return redirect("/messages/room?id={0}".format(thread_id))

@message_view.route("/messages/room")
@login_required
def view_chat():
    # Fetch messages for the specific chat thread
    thread_id = request.args.get("id")
    if not messages_control.is_in_thread(thread_id,current_user.id):
        print("kicked")
        return redirect("/messages")
    
    chat_messages = messages_control.pull_messages_from_db_by_thread(thread_id)
    chat_recipient_id, chat_recipient_name = messages_control.get_recipient_id_and_name(thread_id, current_user.id)
    return render_template("chat_detail.html", messages=chat_messages,
                chat_recipient_id=chat_recipient_id, chat_recipient_name=chat_recipient_name,
            my_id=current_user.id, my_name=current_user.name, thread_id=thread_id)
    # return render_template("message/message_detail.html", messages=chat_messages,
    #             chat_recipient_id=chat_recipient_id, chat_recipient_name=chat_recipient_name,
    #         my_id=current_user.id, my_name=current_user.name, thread_id=thread_id)

@socketio.on("send_message", namespace="/messages/room")
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

    #recipient_websocket_id = user_control.websocket_id_query(data.get('recipient_id'))

    socketio.emit(f"{thread_id}_newmsg",
                  {'message': data.get('message'),
                   'recipient_id' : message.recipient_id,
                   'recipient_name' : data.get('chat_recipient_name'),
                   'sender_name' : current_user.name,
                   'timestamp' : timestamp.strftime('%m/%d %H:%M:%S')
                   }, 
                  namespace='/messages/room')
    return jsonify({"status": "Message sent", "thread_id": thread_id}), 200

@message_view.route("/messages/fetch/<thread_id>")
@login_required
def fetch_messages(thread_id):
    messages = messages_control.pull_messages_from_db_by_thread(thread_id)
    if messages:
        return jsonify([message.__dict__ for message in messages]), 200
    else:
        return jsonify({"error": "Failed to fetch messages"}), 500

@message_view.route("/messages/read/<thread_id>", methods=["POST"])
@login_required
def mark_messages_as_read(thread_id):
    messages_control.mark_thread_as_read(thread_id, current_user.id)
    return jsonify({"status": "Messages marked as read"}), 200
