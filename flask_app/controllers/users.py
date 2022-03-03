from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.story_model import Story
from flask_app.models.comment_model import Comment
from flask_app.controllers import stories
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# DISPLAY ROUTES
@app.route('/')
def display_home():
    return render_template("home.html")

@app.route('/display_login')
def display_login():
    if 'user_id' in session:
        return redirect('/display_explore')
    return render_template("login.html")

@app.route('/display_register')
def display_register():
    if 'user_id' in session:
        return redirect('/display_explore')
    return render_template('register.html')

@app.route('/display_explore')
def display_explore():
    if 'user_id' not in session:
        return redirect('/display_login')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    stories = Story.get_all_with_all_users()
    return render_template('explore.html', loggedin_user=loggedin_user, stories=stories)

@app.route('/display_explore_sorted_az')
def display_explore_sorted_az():
    if 'user_id' not in session:
        return redirect('/display_login')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    stories = Story.get_all_with_all_users_sorted_by_a_thru_z()
    return render_template('explore.html', loggedin_user=loggedin_user, stories=stories)

@app.route('/display_explore_sorted_category')
def display_explore_sorted_category():
    if 'user_id' not in session:
        return redirect('/display_login')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    stories = Story.get_all_with_all_users_sorted_by_category()
    return render_template('explore.html', loggedin_user=loggedin_user, stories=stories)

@app.route('/display_account')
def display_loggedin_user_account():
    if 'user_id' not in session:
        return redirect('/display_login')
    loggedin_user = User.get_by_id({"id" : session['user_id']})
    user_stories = User.get_one_with_stories_created({'id' : int(session['user_id'])})
    return render_template('account.html', loggedin_user=loggedin_user, user_stories=user_stories)

@app.route('/display_about')
def display_about():
    return render_template('about.html')




#********************************************************************


#***************************************************************************************************    
# ACTION ROUTES: never render on action route, only redirect
@app.route('/register_user', methods=["POST"])
def register_user():
    if not User.validate_user_registration(request.form):
        return redirect('/display_register')
    data = {
        "first_name": request.form["register_first_name"],
        "last_name" : request.form["register_last_name"],
        "email" : request.form["register_email"],
        "password" : request.form["register_password"]
    }
    User.save(data)
    loggedin_user = User.get_by_email(data)
    session['user_id'] = loggedin_user.id
    return redirect('/display_explore')

@app.route('/login_user', methods=["POST"])
def login_user():
    data = {
        "email" : request.form['login_email'],
        "password" : request.form['login_password']
    }
    if not User.validate_login(data):
        return redirect('/display_login')
    else:
        data = {
            "email" : request.form["login_email"]
        }
        loggedin_user = User.get_by_email(data)
        session['user_id'] = loggedin_user.id
        return redirect('/display_explore')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/display_login')

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'user_id' not in session:
            return redirect('/')
    data = {
        "id" : session['user_id'],
        "first_name" : request.form['update_first_name'],
        "last_name" : request.form['update_last_name'],
        "email" : request.form['update_email'],
        "password" : request.form['update_password'],
        "confirm_password" : request.form['update_confirm_password']
    }
    if not User.validate_update_user(data):
        return redirect('/display_account')
    data2 = {
        "id" : session['user_id'],
        "first_name" : request.form['update_first_name'],
        "last_name" : request.form['update_last_name'],
        "email" : request.form['update_email'],
        "password" : bcrypt.generate_password_hash(request.form['update_password']),
        "confirm_password" : request.form['update_confirm_password']
    }
    User.update_user_account(data2)
    return redirect("/display_account")


#********************************************************************************************************




#***********************************************************************************************

#for testing only: ###############################################################################
@app.route('/test_one')
def testing():
    user_magazines = User.get_one_with_magazines_created({'id' : int(session['user_id'])})
    print("AHHHHHH:", user_magazines)
    return "test"


