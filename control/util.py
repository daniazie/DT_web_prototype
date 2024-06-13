import json

def load_lang_dict(page_name,lang):
    path = "dictionary/{0}.json".format(page_name)
    try:
        with open(path, 'r', encoding='UTF8') as file:
            data = json.load(file)
            return data[lang]
    except Exception as e :
        print(e)
        return None
