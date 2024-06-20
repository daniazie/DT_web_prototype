from flask import Flask, request, redirect, render_template, Blueprint, flash
from flask_login import login_required, current_user
from control import lang_control,post_control
from models import post

post_detail_view = Blueprint("post_detail_view", __name__)

@post_detail_view.route("/post_detail")
@login_required
def post_detail():
    labels = lang_control.load_lang_dict("posts")
    post_id = int(request.args.get('post_id',0))
    post_info = post_control.pull_post_from_db_by_postID(post_id)
    post_info.job_info = lang_control.translate_post(post_info.job_info)
    post_content = post_control.pull_content_from_db(post_id)

    return render_template("/posts/post_detail.html",
                           post=post_info,post_content=post_content,user=current_user,labels=labels)
    


@post_detail_view.route("/post_detail/delete")
@login_required
def post_delete():
    post_id = int(request.args.get('post_id',0))
    
    if post_control.delete_post(post_id):
        flash("SUC_CODE:POST_DELETED",category="success")
    else:
        flash("ERR_CODE:FAILED_TO_DELETE_POST",category="error")
    
    return redirect("/posts")