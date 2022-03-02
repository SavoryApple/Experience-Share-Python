from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.story_model import Story
from flask_app.models.comment_model import Comment


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
