import json
from flask import request
from models import post, user, language

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
    
def translate_post(job:post.Post_job_info):
    lang = request.cookies.get('selected_lang')
    path = "dictionary/_post.json"
    data = {}
    new_job = job
    try:
        with open(path, 'r', encoding='UTF8') as file:
            data.update(json.load(file)[lang])
            new_job.time_unit = data[job.time_unit]
            print(job.lang_level)
            print(job.lang_level.split(" - "))
            print([data[x] for x in job.lang_level.split(" - ")])
            new_job.lang_level = " - ".join([data[x] for x in job.lang_level.split(" - ")])
            print(new_job.lang_level)
            if new_job.working_days.count(','):
                new_job.working_days = ','.join([data[x] for x in job.working_days.split(',')])
            else:
                new_job.working_days = data[job.working_days]
                
        return new_job

    except Exception as e :
        print(e)
        return job

def translate_profile(user:user.User):
    lang = request.cookies.get('selected_lang')
    path = "dictionary/_profile.json"
    data = {}
    new_user = user
    try:
        with open(path, 'r', encoding='UTF8') as file:
            data.update(json.load(file)[lang])
            new_user.city = data[user.city]
            new_user.country = data[user.country]
            new_user.gender = data[user.gender]
            print(language.convert_code_to_lang(user.language))
            new_user.language = data[language.convert_code_to_lang(user.language)]
        return new_user

    except Exception as e :
        print(e)
        return user