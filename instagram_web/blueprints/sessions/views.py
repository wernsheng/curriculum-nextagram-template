from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import check_password_hash


# from models.user import User


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    username = request.form['username'] 
    # user_password = request.form['user_password']
    user = User.get_or_none (User.username == username)
    password_to_check = request.form['user_password'] # password keyed in by the user in the sign in form
    hashed_password = user.password # password hash stored in database for a specific user
    if user and check_password_hash(hashed_password, password_to_check):  # what is result? Test it in Flask shell and implement it in your view function!
        flash("Successfully logged in")
        return redirect ("/")
    else:
        return '<h1> Failed Login </h1>' 
        
    # print (result)

    # if user.save():
    #     flash("Successfully saved")
    #     return redirect (url_for('/<username>'))
    # else: 
    #     return render_template ('new.html')