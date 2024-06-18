from flask import Flask, request, redirect, render_template, Blueprint, flash
from flask_login import login_required, current_user
from control import lang_control, community_control
from models.socketio import socketio
from models import community

community_view = Blueprint("community_view", __name__)
_MAX_POST_IN_SINGLE_PAGE = 6

@community_view.route("/community")
@login_required
def home():
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)
    my_comm_list = community_control.pull_community_list_from_db(current_user.id)
    sug_comm_list = community_control.get_suggested_community_list(current_user.id,3)

    return render_template("community/community.html",user=current_user,labels=labels,
                           my_comm_list=my_comm_list,sug_comm_list=sug_comm_list)

@community_view.route("/community/comm")
@login_required
def comm():
    community_id = request.args.get('id')
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)
    page_max = community_control.count_post(community_id) // _MAX_POST_IN_SINGLE_PAGE + 1
    current_page = int(request.args.get('pages',1))

    comm = community_control.pull_community_from_db(community_id)
    comm_post_list = community_control.pull_community_post_list_from_db_rows(
            community_id, _MAX_POST_IN_SINGLE_PAGE,
            start=(current_page-1)*_MAX_POST_IN_SINGLE_PAGE
            )
    
    pagination_start = max(1,current_page-3)
    pagination_end = min(pagination_start+6,page_max)
    
    return render_template("community/community-posts.html",user=current_user,labels=labels,
                            comm=comm,comm_post_list=comm_post_list,
                            pagination_start=pagination_start,
                            pagination_end=pagination_end,
                            page_max=page_max, current_page=current_page)

@community_view.route("/community/post")
@login_required
def comm_detail():
    labels = lang_control.load_lang_dict("community",lang_control.selected_lang)

    community_id = request.args.get('cid')
    c_post_id = request.args.get('pid')
    comm = community_control.pull_community_from_db(community_id)
    comm_post = community_control.pull_community_post(c_post_id)
    comm_comment = community_control.pull_community_post_comment_from_db(c_post_id)
    is_like = community_control.is_like_post(current_user.id,c_post_id)

    return render_template("community/community-detail.html",user=current_user,labels=labels,
                           comm=comm,comm_post=comm_post,comm_comment=comm_comment,
                           is_like=is_like)

@community_view.route("/community/add-post", methods = ['GET', 'POST'])
@login_required
def comm_post():
    labels = lang_control.load_lang_dict("add-post",lang_control.selected_lang)

    community_id = request.args.get('id')
    if not community_id:
        community_id = request.form.get('community_id')

    comm = community_control.pull_community_from_db(community_id)
    print(request.form.get('content'))
    if request.form.get('content') and request.method == "POST":
        if not community_control.is_member(community_id,current_user.id):
            redirect("/community")

        data = community.Community_post()
        data.community_id = community_id
        data.writer_id = current_user.id
        data.writer_name = current_user.name
        data.content = request.form.get('content')
        community_control.push_community_post(data)
        return redirect("/community/comm?id={0}".format(community_id))
    else :
        return render_template("community/add-community-post.html",user=current_user,labels=labels,
                               comm=comm)
        

@community_view.route("/community/join")
@login_required
def comm_join():
    community_id = request.args.get('id')
    if community_control.join_community(community_id,current_user.id):
        flash("SUC_CODE:POST_UPLOADED", category='success')
    else:
        flash("ERR_CODE:FAILED_TO_JOIN_COMM", category='error')

    return redirect("/community")


@socketio.on("c_post_like")
def post_like(data):
    print("like")
    c_post_id = data.get("c_post_id")
    writer_id = data.get("writer_id")
    
    result = community_control.toggle_post_like(writer_id,c_post_id)
    
    socketio.emit("c_post_like_response",{},to=request.sid)

@socketio.on("c_post_comment")
def post_comment(data):
    print("comment")
    comment = community.Community_post_comment()
    comment.c_post_id = data.get("c_post_id")
    comment.comment = data.get("comment")
    comment.writer_id = data.get("writer_id")
    comment.writer_name = data.get("writer_name")

    result = community_control.push_community_post_comment(comment)

    socketio.emit("c_post_comment_response",{
                  'writer_name' : comment.writer_name,
                  'comment' : comment.comment},to=request.sid)
    