from flask import Flask, request, redirect, render_template, Blueprint
from flask_login import login_required, current_user
from control import post_control
from models import post

add_post_view = Blueprint("add_post_view", __name__)

@add_post_view.route("/posts/add_post", methods = ['GET', 'POST'])
@login_required
def add_post():
    if request.method == "POST":
        workplace = request.form.get('shop-name')
        location = request.form.get('location')
        pay = request.form.get('payrate')

        working_days = ','.join(request.form.getlist('days'))
        working_hours = '{0} ~ {1}'.format(
            request.form.get('working-time-start'),
            request.form.get('working-time-end')
            )
        
        lang_type_l = request.form.getlist('level-language')
        lang_level_l = request.form.getlist('language-preferred')
        temp_list = []
        for i in range(len(lang_type_l)):
            temp_list.append("{0} - {1}".format(lang_type_l[i],lang_level_l[i]))
        lang_level = ' , '.join(temp_list)

        content = request.form.get('description')

        isEmpty = post_control.is_empty(workplace,location,pay,working_days,
                                        working_hours,content,lang_level,content)

        if isEmpty:
            print("Something is EMPTY")
            return redirect("/posts/add_post")
        
        job_info = post.Post_job_info()
        job_info.location = location
        job_info.pay = pay
        job_info.time_unit = "Hour"
        job_info.lang_level = lang_level
        job_info.working_days = working_days
        job_info.working_hours = working_hours
        job_info.workplace = workplace

        _post = post.Post()
        _post.writer = current_user.id
        _post.type = post.POST_TYPE_JOB
        _post.preview = content[0:max(98,len(content))]
        _post.job_info = job_info

        post_content = post.Post_content
        post_content.content = content
        post_content.origin = True
        post_content.language = current_user.language
        post_content.contributer = current_user.id

        result = post_control.push_post_to_db(_post,post_content)

        if result:
            return redirect("/posts")
        else:
            return redirect("/posts/add_post")
    else:
        return render_template("add-post.html")