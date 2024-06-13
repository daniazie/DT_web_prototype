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
    
    sql_post_head = "INSERT INTO Posts_head(type,writer,preview)\
         VALUE({0},'{1}','{2}')".format(
            _post.type,
            _post.writer,
            _post.preview
        )
    success, e = con.execute_with_commit(sql_post_head)
    if not success:
        print(e)
        return success

    post_id = con.execute_select_one("SELECT post_id FROM Posts_head WHERE writer='{0}' and preview='{1}'"
                                    .format(_post.writer,_post.preview))

    if post_id != None:
        post_id = post_id['post_id']
        sql_post_job = "INSERT INTO Posts_job_info(post_id,location,pay,time_unit,\
            working_hours,lang_level,working_days,workplace)\
             VALUE({0},'{1}',{2},'{3}','{4}','{5}','{6}','{7}')".format(
                post_id,
                _post.job_info.location,
                _post.job_info.pay,
                _post.job_info.time_unit,
                _post.job_info.working_hours,
                _post.job_info.lang_level,
                _post.job_info.working_days,
                _post.job_info.workplace
             )
        success, e = con.execute_with_commit(sql_post_job)
        if not success:
            print(e)
            return success
        
        sql_post_content = "INSERT INTO Posts_content(post_id,content,origin,language,contributer)\
             VALUE({0},'{1}',{2},'{3}','{4}')".format(
                post_id,
                post_content.content,
                post_content.origin,
                post_content.language,
                post_content.contributer
             )
        success, e = con.execute_with_commit(sql_post_content)
        if not success:
            print(e)
            return success
        else :
            return success
        
def count_post():
    con = db.DataBase()
    result = con.count_select_rows("SELECT * FROM Posts_head")
    return result

def delete_post(post_id):
    con = db.DataBase()
    result = con.execute_with_commit("DELETE FROM Posts_head WHERE post_id = {0}".format(post_id))
    return result

def is_empty(*args):
    result = False
    
    for i in args:
        result = result or (i == "") or (i == None)
    
    return result