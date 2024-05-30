import models.post as post
import models.database as db

def __convert_dict_to_post(dict):
    data = post.Post()
    data.post_id = dict['post_id']
    data.date = dict['date']
    data.type = dict['type']
    data.writer = dict['writer']
    data.preview = dict['preview']
    return data

def __convert_dict_to_job_info(dict):
    data = post.Post_job_info()
    data.post_id = dict['post_id']
    data.time_unit = dict['time_unit']
    data.pay = dict['pay']
    data.place = dict['place']
    data.lang_level = dict['lang_level']
    data.working_days = dict['working_days']
    data.working_hours = dict['working_hours']
    return data

def __add_job_info_to_post(data, con):
    if data.type == post.POST_TYPE_JOB:
        result = con.execute_select_one("SELECT * FROM Posts_job_info WHERE post_id='{0}'"
                                            .format(data.post_id))
        data.job_info = __convert_dict_to_job_info(result)
    return data

def pull_post_from_db_by_postID(post_id):
    con = db.DataBase()
    result = con.execute_select_one("SELECT * FROM Posts_head WHERE post_id='{0}'"
                                    .format(post_id))
    if result: 
        data = __convert_dict_to_post(result)
        data = __add_job_info_to_post(data, con)
    else: # failed to search id from database
        return None

def pull_post_from_db_by_userID(user_id):
    con = db.DataBase()
    result = con.execute_select_all("SELECT * FROM Posts_head WHERE writer='{0}'"
                                    .format(user_id))
    if result: 
        post_lst = []
        for i in result:
            data = __convert_dict_to_post(i)
            data = __add_job_info_to_post(data, con)
            post_lst.append(data)
        return post_lst
    else:
        return None
    
def pull_post_from_db_rows(n):
    con = db.DataBase()
    result = con.execute_select_all("SELECT * FROM Posts_head ORDER BY post_id DESC limit {0}"
                                    .format(n))
    if result: 
        post_lst = []
        for i in result:
            data = __convert_dict_to_post(i)
            if data.type == post.POST_TYPE_JOB:
                data = __add_job_info_to_post(data, con)
                post_lst.append(data)
        return post_lst
    else:
        return None
    
