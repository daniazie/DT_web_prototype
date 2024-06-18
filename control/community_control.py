from models import community, database as db
import random

def __convert_dict_to_community(dict):
    data = community.Community_head()
    data.community_id = dict['community_id']
    data.community_name = dict['community_name']
    data.community_desc = dict['community_desc']
    return data

def __get_coummnity_number_members(community_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_member WHERE community_id = {0}"
    result = con.count_select_rows(sql.format(community_id))
    return result

def pull_community_from_db(community_id):
    con = db.DataBase()
    sql = "SELECT * FROM Community_head WHERE community_id = {0}"
    result = con.execute_select_one(sql.format(community_id))
    result = __convert_dict_to_community(result)
    result.number_members = __get_coummnity_number_members(result.community_id)
    return result

def pull_community_list_from_db(user_id=None,match=True):
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

    for i in range(len(result)):
        result[i] = __convert_dict_to_community(result[i])
        result[i].number_members = __get_coummnity_number_members(result[i].community_id)

    return result

def get_suggested_community_list(user_id,num):
    community_list = pull_community_list_from_db(user_id,False)
    list_len = len(community_list)

    if list_len > 0:
        return random.sample(community_list,min(num,list_len))
    else :
        return []
    



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
