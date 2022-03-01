from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.story_model import Story
from flask_app.controllers import stories

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
    stories = User.get_all_with_stories_created()
    return render_template('explore.html', loggedin_user=loggedin_user, stories=stories)

@app.route('/display_account')
def display_loggedin_user_account():
    if 'user_id' not in session:
        return redirect('/dispay_login')
    return render_template('account.html')

@app.route('/display_about')
def display_about():
    return render_template('about.html')







#********************************************************************




@app.route('/dashboard')
def display_dashboard():
    if 'user_id' not in session:
            return redirect('/')
    magazines = Magazine.get_all_magazines_and_creators()
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    return render_template("dashboard.html", magazines=magazines, loggedin_user=loggedin_user)

@app.route('/user/account')
def display_accountt():
    if 'user_id' not in session:
            return redirect('/')
    loggedin_user = User.get_by_id({'id' : int(session['user_id'])})
    user_magazines = User.get_one_with_magazines_created({'id' : int(session['user_id'])})
    return render_template('account.html', loggedin_user = loggedin_user, user_magazines=user_magazines)
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
    return redirect('/')


#********************************************************************************************************


@app.route('/update_account_action', methods=['POST'])
def update_account():
    if "user_id" not in session:
        return redirect('/')
    
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "id" : session['user_id']
    }
    if not User.validate_update_user(data):
        return redirect('/user/account')
    User.update_user(data)
    return redirect("/user/account")




#***********************************************************************************************

#for testing only: ###############################################################################
@app.route('/test_one')
def testing():
    user_magazines = User.get_one_with_magazines_created({'id' : int(session['user_id'])})
    print("AHHHHHH:", user_magazines)
    return "test"


