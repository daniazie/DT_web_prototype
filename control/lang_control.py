import json
from models.socketio import socketio

selected_lang = "en"

def load_lang_dict(page_name,lang):
    path = "dictionary/{0}.json"
    data = {}
    try:
        with open(path.format("base"), 'r', encoding='UTF8') as file:
            data.update(json.load(file)[lang])
        with open(path.format(page_name), 'r', encoding='UTF8') as file:
            data.update(json.load(file)[lang])
        return data
    except Exception as e :
        print(e)
        return None

@socketio.on('lang_selected')
def lang_selected(data):
    global selected_lang
    selected_lang = data.get("lang")
    socketio.emit("lang_selected_response","")