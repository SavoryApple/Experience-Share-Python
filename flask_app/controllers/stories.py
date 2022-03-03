from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.story_model import Story
from flask_app.models.comment_model import Comment
from flask_app.models.story_vote_model import story_Vote
from flask_app.controllers import users


# DISPLAY ROUTES###############################################################################################
@app.route('/display_create')
def display_create():
    if 'user_id' not in session:
        return redirect('/display_login')
    return render_template('create_story.html')

@app.route('/show/<int:story_id>')
def display_view(story_id):
    if "user_id" not in session:
        return redirect('/')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    story_info = Story.get_one_with_creator({"id" : int(story_id)})
    comments = Comment.get_all_with_all_users({"story_id" : int(story_id)})
    data = {
        "story_id" : story_id,
        "user_id" : session['user_id']
    }
    votes = story_Vote.sum_all_votes_with_story_id(data)
    return render_template("view_story.html", story_info=story_info, loggedin_user=loggedin_user, comments=comments, votes=votes)

@app.route('/display_update/<int:story_id>')
def display_update(story_id):
    if 'user_id' not in session:
        return redirect('/display_login')
    story_info = Story.get_story_by_id({'id' : int(story_id)})
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    return render_template('update_story.html', story_info=story_info, loggedin_user=loggedin_user)


##############################################################################################################


# ACTION ROUTES################################################################################################
@app.route('/create_story', methods=['POST'])
def create_story():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "category" : request.form['category'],
        "item_name" : request.form['item_name'],
        "place_purchased" : request.form['place_purchased'],
        "img_url" : request.form['img_url'],
        "story" : request.form['your_story'],
        "creator_id" : session['user_id']
    }
    if not Story.validate_create_story(data):
        return redirect('/display_create')
    Story.save(data)
    return redirect("/display_explore")

@app.route('/update_story/<int:story_id>', methods=['POST'])
def update_story(story_id):
    data = {
        "id" : story_id,
        "category" : request.form['category'],
        "item_name" : request.form['item_name'],
        "place_purchased" : request.form['place_purchased'],
        "img_url" : request.form['img_url'],
        "story" : request.form['your_story'],
        "creator_id" : session['user_id']
    }
    if not Story.validate_create_story(data):
        return redirect(f'/display_update/{story_id}')
    Story.update_story(data)
    return redirect('/display_explore')

@app.route('/delete_story/<int:story_id>')
def delete_story(story_id):
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "id" :story_id
    }
    Story.delete_story(data)
    return redirect('/display_explore')

@app.route('/delete_account_story/<int:story_id>')
def delete_account_story(story_id):
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "id" :story_id
    }
    Story.delete_story(data)
    return redirect('/display_account')

@app.route('/upvote/<int:story_id>')
def upvote(story_id):
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "story_id" :story_id,
        "user_id" : session['user_id']
    }
    story_Vote.upvote_on_story_from_user(data)
    return redirect(f'/show/{story_id}')

@app.route('/downvote/<int:story_id>')
def downvote(story_id):
    if "user_id" not in session:
        return redirect('/display_login')
    data = {
        "story_id" :story_id,
        "user_id" : session['user_id']
    }
    story_Vote.downvote_on_story_from_user(data)
    return redirect(f'/show/{story_id}')

#################################################################################################################




#for testing only: ###############################################################################
@app.route('/test_two')
def test():
    story_info = Story.get_one_with_creator({"id" : 5})
    print("AHHHHHHHHHHHH:", story_info)
    
    return "test"
