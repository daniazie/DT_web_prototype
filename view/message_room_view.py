from flask import Flask, request, jsonify, render_template, Blueprint
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

message_room_view = Blueprint("message_room_view", __name__)
socketio = SocketIO(logger=True, engineio_logger=True)

@message_room_view.record_once
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
    
@message_room_view.route("/messages/<thread_id>")
@login_required
def view_chat(thread_id):
    # Fetch messages for the specific chat thread
    chat_messages = messages_control.pull_messages_from_db_by_thread(thread_id)
    chat_recipient_name = messages_control.get_chat_recipient_name(current_user.id)
    return render_template("chat_detail.html", messages=chat_messages, chat_recipient_name=chat_recipient_name, thread_id=thread_id)

@socketio.on("send_message", namespace="/messages/<thread_id>")
def send_message(data):
    print("send_message recieved")
    thread_id = data.get('thread_id') or randstrurl()
    message=data.get('message')
    print(message)
    message = messages.Messages(
        msg_id=str(uuid4()),
        sender_id=current_user.id,
        recipient_id=data.get('recipient_id'),
        message=data.get('message'),
        thread_id=thread_id,
        timestamp=datetime.now()
    )

    if not messages_control.push_messages_to_db(message):
        return jsonify({"error": "Failed to send message"}), 500

    recipient_websocket_id = user_control.websocket_id_query(data.get('recipient_id'))

    socketio.emit(f"{recipient_websocket_id}_newmsg", {'message': data.get('message'), 'thread_id': thread_id}, namespace='/messages')
    socketio.emit(f"{current_user.websocket_id}_newmsg", {'message': data.get('message'), 'thread_id': thread_id}, namespace='/messages')
    return jsonify({"status": "Message sent", "thread_id": thread_id}), 200

@message_room_view.route("/messages/fetch/<thread_id>")
@login_required
def fetch_messages(thread_id):
    messages = messages_control.pull_messages_from_db_by_thread(thread_id)
    if messages:
        return jsonify([message.__dict__ for message in messages]), 200
    else:
        return jsonify({"error": "Failed to fetch messages"}), 500

@message_room_view.route("/messages/read/<thread_id>", methods=["POST"])
@login_required
def mark_messages_as_read(thread_id):
    messages_control.mark_thread_as_read(thread_id, current_user.id)
    return jsonify({"status": "Messages marked as read"}), 200
