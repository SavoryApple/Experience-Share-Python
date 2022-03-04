from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.comment_vote_model import comment_Vote
from flask_app.models.user_model import User
from flask_app.models.story_model import Story
from flask_app.models.comment_model import Comment
from flask_app.models.story_vote_model import story_Vote

# DISPLAY ROUTES #########################################################################################
@app.route('/show/<int:story_id>/<int:comment_id>')
def display_view_story_with_comment_sum(story_id, comment_id):
    if "user_id" not in session:
        return redirect('/')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    story_info = Story.get_one_with_creator({"id" : int(story_id)})
    comments = Story.get_one_with_users_and_comments_and_sum_votes({"story_id" : int(story_id)})
    data = {
        "story_id" : story_id,
        "user_id" : session['user_id']
    }
    story_Vote.create_vote_with_user(data)
    votes = story_Vote.sum_all_votes_with_story_id(data)
    data = {
        "comment_id" : comment_id,
        "user_id" : session['user_id']
    }
    comment_Vote.create_vote_comment_with_user(data)
    return render_template("view_story_with_comment_votes.html", story_info=story_info, loggedin_user=loggedin_user, comments=comments, votes=votes)


# ACTION ROUTES################################################################################################
@app.route('/save_comment/<int:story_id>', methods=['POST'])
def save_comment(story_id):
    data = {
        "content" : request.form['comment'],
        "user_id" : session['user_id'],
        "story_id" : story_id
    }
    if not Comment.validate_create_comment(data):
        return redirect(f'/show/{story_id}')
    Comment.save(data)
    return redirect(f'/show/{story_id}')

@app.route('/upvote/<int:comment_id>/<int:story_id>')
def upvote_comment(comment_id, story_id):
    print("COMMENT ID, STORY ID:", comment_id, story_id)
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "comment_id" :comment_id,
        "user_id" : session['user_id']
    }
    comment_Vote.create_vote_comment_with_user(data)
    comment_Vote.upvote_comment_on_story_from_user(data)
    return redirect(f'/show/{story_id}/{comment_id}')

@app.route('/downvote/<int:comment_id>/<int:story_id>')
def downvote_comment(comment_id, story_id):
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "comment_id" :comment_id,
        "user_id" : session['user_id']
    }
    comment_Vote.create_vote_comment_with_user(data)
    comment_Vote.downvote_comment_on_story_from_user(data)
    return redirect(f'/show/{story_id}/{comment_id}')
