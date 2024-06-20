import json, time
from flask import request, session

selected_lang = "en"

def load_lang_dict(page_name):
    lang = request.cookies.get('selected_lang')
    if not lang:
        lang = "en"
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
    
# def change_lang(lang_selected):
#     session.update({'lang_selected' : })
#     session.modified = True

# @socketio.on('lang_selected')
# def lang_selected(data):
#     print("called socket")
#     #global selected_lang
#     #selected_lang = data.get("lang")
#     change_lang(data.get("lang"))
#     socketio.emit("lang_selected_response","",to=request.sid)
#     print(session['lang_selected'])