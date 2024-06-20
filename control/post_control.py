import models.post as post
import models.database as db

def __convert_dict_to_post(dict):
    data = post.Post()
    data.post_id = dict['post_id']
    data.date = dict['date']
    data.type = dict['type']
    data.writer_id = dict['writer_id']
    data.writer_name = dict['writer_name']
    data.preview = dict['preview']
    return data

def __convert_dict_to_job_info(dict):
    data = post.Post_job_info()
    data.post_id = dict['post_id']
    data.time_unit = dict['time_unit']
    data.pay = dict['pay']
    data.location = dict['location']
    data.lang_level = dict['lang_level']
    data.working_days = dict['working_days']
    data.working_hours = dict['working_hours']
    data.workplace = dict['workplace']
    return data

def __convert_dict_to_post_content(dict):
    data = post.Post_content()
    data.post_id = dict['post_id']
    data.content = dict['content']
    data.origin = dict['origin']
    data.language = dict['language']
    data.contributer = dict['contributer']
    data.like = dict['like']
    data.unlike = dict['unlike']
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
        return data
    else: # failed to search id from database
        return None

def pull_post_from_db_by_userID(user_id):
    con = db.DataBase()
    result = con.execute_select_all("SELECT * FROM Posts_head WHERE writer_id='{0}'"
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
    
def pull_post_from_db_rows(n, start=0):
    con = db.DataBase()
    result = con.execute_select_all("SELECT * FROM Posts_head ORDER BY post_id DESC limit {0} OFFSET {1}"
                                    .format(n,start))
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
    
def pull_content_from_db(post_id):
    con = db.DataBase()
    result = con.execute_select_one("SELECT * FROM Posts_content WHERE post_id='{0}'"
                                    .format(post_id))
    if result: 
        data = __convert_dict_to_post_content(result)
        return data
    else: # failed to search id from database
        return None

def push_post_to_db(_post: post.Post, post_content: post.Post_content):
    con = db.DataBase()
    
    sql_post_head = "INSERT INTO Posts_head(type,writer_id,preview,writer_name)\
         VALUE({0},'{1}','{2}','{3}')".format(
            _post.type,
            _post.writer_id,
            db.add_escape(_post.preview),
            db.add_escape(_post.writer_name)
        )
    result, e = con.execute_with_commit(sql_post_head)
    if not result:
        print(e)
        return result

    post_id = con.execute_select_one("SELECT post_id FROM Posts_head WHERE writer_id='{0}' and preview='{1}'"
                                    .format(_post.writer_id,db.add_escape(_post.preview)))

    if post_id != None:
        post_id = post_id['post_id']
        sql_post_job = "INSERT INTO Posts_job_info(post_id,location,pay,time_unit,\
            working_hours,lang_level,working_days,workplace)\
             VALUE({0},'{1}',{2},'{3}','{4}','{5}','{6}','{7}')".format(
                post_id,
                db.add_escape(_post.job_info.location),
                _post.job_info.pay,
                _post.job_info.time_unit,
                _post.job_info.working_hours,
                _post.job_info.lang_level,
                _post.job_info.working_days,
                db.add_escape(_post.job_info.workplace)
             )
        print()
        result, e = con.execute_with_commit(sql_post_job)
        if not result:
            print(e)
            return result
        
        sql_post_content = "INSERT INTO Posts_content(post_id,content,origin,language,contributer)\
             VALUE({0},'{1}',{2},'{3}','{4}')".format(
                post_id,
                db.add_escape(post_content.content),
                post_content.origin,
                post_content.language,
                post_content.contributer
             )
        result, e = con.execute_with_commit(sql_post_content)
        if not result:
            print(e)
            return result
        else :
            return result
        
def count_post():
    con = db.DataBase()
    result = con.count_select_rows("SELECT * FROM Posts_head")
    return result

def delete_post(post_id):
    con = db.DataBase()
    result = con.execute_with_commit("DELETE FROM Posts_head WHERE post_id = {0}".format(post_id))
    return result

def change_days_list_to_str(days_list):
    if days_list == None:
        return None
    result = ""
    for i in days_list:
        result = result + i[0:3] + ","

    result = result[:-1]

    if result.lower() == "Mon,Tue,Wed,Thu,Fri,Sat,Sun".lower():
        result = "Everyday"
    elif result.lower() == "Mon,Tue,Wed,Thu,Fri".lower():
        result = "Weekdays"
    elif result.lower() == "Sat,Sun".lower():
        result = "Weekends"

    return result
    

def is_empty(*args):
    result = False
    
    for i in args:
        result = result or (i == "") or (i == None)
    
    return result