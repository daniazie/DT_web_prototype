from models import community, database as db
import random

def __get_coummnity_number_members(community_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_member WHERE community_id = {0}"
    result = con.count_select_rows(sql.format(community_id))
    return result

def __get_coummnity_post_number_like(c_post_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_post_like WHERE c_post_id = {0}"
    result = con.count_select_rows(sql.format(c_post_id))
    return result

def __get_coummnity_post_number_comments(c_post_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_post_comment WHERE c_post_id = {0}"
    result = con.count_select_rows(sql.format(c_post_id))
    return result

def __convert_dict_to_community(dict):
    data = community.Community_head()
    data.community_id = dict['community_id']
    data.community_name = dict['community_name']
    data.community_desc = dict['community_desc']
    data.number_members = __get_coummnity_number_members(data.community_id)
    return data

def __convert_dict_to_community_post(dict):
    data = community.Community_post()
    data.c_post_id = dict['c_post_id']
    data.community_id = dict['community_id']
    data.date = dict['date']
    data.content = dict['content']
    data.writer_id = dict['writer_id']
    data.writer_name = dict['writer_name']
    data.number_comments = __get_coummnity_post_number_comments(data.c_post_id)
    data.number_like = __get_coummnity_post_number_like(data.c_post_id)
    return data

def __convert_dict_to_community_post_comment(dict):
    data = community.Community_post_comment()
    data.c_post_id = dict['c_post_id']
    data.comment = dict['comment']
    data.date = dict['date']
    data.writer_id = dict['writer_id']
    data.writer_name = dict['writer_name']
    return data

def is_member(community_id,user_id):
    con = db.DataBase()
    result = con.count_select_rows("SELECT * Community_member \
                                   WHERE community_id = {0} AND user_id = '{1}'"
                                   .format(community_id, user_id))
    if result > 0:
        return True
    else :
        return False

def pull_community_from_db(community_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_head WHERE community_id = {0}"
    result = con.execute_select_one(sql.format(community_id))
    result = __convert_dict_to_community(result)
    result.number_members = __get_coummnity_number_members(result.community_id)
    return result

def pull_community_list_from_db(user_id=None,match=True):
    comm_list = []
    con = db.DataBase()
    sql = "SELECT * FROM Community_head"

    if user_id:
        if match:
            sql = "SELECT Community_head.* FROM Community_head \
        JOIN Community_member ON Community_head.community_id = Community_member.community_id \
        WHERE Community_member.user_id = '{0}'"
        else :
            sql = "SELECT Community_head.* FROM Community_head \
        LEFT JOIN Community_member ON Community_head.community_id = Community_member.community_id\
        AND Community_member.user_id = '{0}' WHERE Community_member.user_id IS NULL"

    result = con.execute_select_all(sql.format(user_id))
    if not result : return []

    for i in result:
        comm_list.append(__convert_dict_to_community(i))

    return comm_list

def get_suggested_community_list(user_id,num):
    community_list = pull_community_list_from_db(user_id,False)
    list_len = len(community_list)

    if list_len > 0:
        return random.sample(community_list,min(num,list_len))
    else :
        return []
    
def pull_community_post(c_post_id):
    con = db.DataBase()
    result = con.execute_select_one("SELECT * FROM Community_post WHERE c_post_id = {0}".format(c_post_id))

    return __convert_dict_to_community_post(result)

def pull_community_post_list_from_db_rows(community_id, n, start=0):
    comm_post_list = []
    con = db.DataBase()
    sql = "SELECT * FROM Community_post WHERE community_id = {0} ORDER BY c_post_id DESC limit {1} OFFSET {2}"

    result = con.execute_select_all(sql.format(community_id,n,start))
    if not result : return []

    for i in result :
        comm_post_list.append(__convert_dict_to_community_post(i))

    return comm_post_list

def count_post(community_id):
    con = db.DataBase()
    result = con.count_select_rows("SELECT * FROM Community_post WHERE community_id = {0}".format(community_id))
    return result

def join_community(community_id, user_id):
    con = db.DataBase()
    sql = "INSERT INTO Community_member(community_id, user_id) VALUE ({0},'{1}')"
    result, e = con.execute_with_commit(sql.format(community_id, user_id))
    print(e)

    return result

def leave_community(community_id, user_id):
    con = db.DataBase()
    sql = "DELETE FROM Community_member WHERE community_id = {0} ANd user_id = '{1}'"
    result, e = con.execute_with_commit(sql.format(community_id, user_id))
    print(e)

    return result

def push_community_post(data):
    con = db.DataBase()
    sql = "INSERT INTO Community_post(community_id, writer_id, writer_name, content)\
        VALUE ({0},'{1}','{2}','{3}')"
    result, e = con.execute_with_commit(sql.format(data.community_id, data.writer_id,
                                                   data.writer_name, data.content))
    print(e)

    return result

def pull_community_post_comment_from_db(c_post_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_post_comment WHERE c_post_id = {0} ORDER BY date DESC "
    comment_list = []
    result = con.execute_select_all(sql.format(c_post_id))
    if result:
        for i in result:
            comment_list.append(__convert_dict_to_community_post_comment(i))

    return comment_list

def is_like_post(user_id, c_post_id):
    con = db.DataBase()
    result = con.count_select_rows("SELECT * FROM Community_post_like WHERE user_id = '{0}' AND c_post_id = {1}"
                                   .format(user_id, c_post_id))
    if result > 0:
        return True
    else :
        return False
    
def toggle_post_like(user_id, c_post_id):
    con = db.DataBase()
    sql = ""
    if is_like_post(user_id, c_post_id):
        sql = "DELETE FROM Community_post_like WHERE user_id = '{0}' AND c_post_id = {1}"
    else :
        sql = "INSERT INTO Community_post_like(user_id, c_post_id) VALUE ('{0}',{1})"

    result,e = con.execute_with_commit(sql.format(user_id, c_post_id))

    return result

def push_community_post_comment(data):
    con = db.DataBase()
    sql = "INSERT INTO Community_post_comment(c_post_id, writer_id, writer_name, comment)\
        VALUE ({0},'{1}','{2}','{3}')"
    result, e = con.execute_with_commit(sql.format(data.c_post_id, data.writer_id,
                                                   data.writer_name, data.comment))
    return result