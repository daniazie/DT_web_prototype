from flask import Flask, request, redirect, render_template, Blueprint
from flask_login import login_required, login_manager
from control import post_control
from models import post

post_detail_view = Blueprint("post_detail_view", __name__)

@post_detail_view.route("/post_detail")
@login_required
def post_detail():
    post_id = int(request.args.get('post_id',0))
    post_info = post_control.pull_post_from_db_by_postID(post_id)
    post_content = post_control.pull_content_from_db(post_id)

    return render_template("/posts/post_detail.html",
                           post=post_info,post_content=post_content)