import json

selected_lang = "en"

def load_lang_dict(page_name,lang):
    path = "dictionary/{0}.json".format(page_name)
    data = []
    try:
        with open(path.format("base"), 'r', encoding='UTF8') as file:
            data = json.load(file)
        with open(path.format("base-login"), 'r', encoding='UTF8') as file:
            data = json.load(file)
        with open(path.format(page_name), 'r', encoding='UTF8') as file:
            data = json.load(file)
        return data[lang]
    except Exception as e :
        print(e)
        return None