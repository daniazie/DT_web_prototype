from flask import Flask, url_for, request, redirect, render_template, Blueprint
from flask_login import login_required, login_manager
from control import post_control
from models import post

posts_view = Blueprint("posts_view", __name__)
_MAX_POST_IN_SINGLE_PAGE = 6

@posts_view.route("/posts")
@login_required
def posts():
    page_max = post_control.count_post() // _MAX_POST_IN_SINGLE_PAGE + 1
    current_page = int(request.args.get('pages',1))
    post_list = post_control.pull_post_from_db_rows(
        _MAX_POST_IN_SINGLE_PAGE, 
        start=(current_page-1)*_MAX_POST_IN_SINGLE_PAGE
        )
    if post_list[-1].post_id == 0:
        post_list.pop()

    pagination_start = max(1,current_page-3)
    pagination_end = min(pagination_start+6,page_max)

    return render_template("posts.html",
                           pagination_start=pagination_start,
                           pagination_end=pagination_end,
                           page_max=page_max,
                           current_page=current_page,
                           post_list=post_list
                           )