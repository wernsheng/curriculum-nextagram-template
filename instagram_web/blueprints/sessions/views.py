from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/login', methods=['GET'])
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
        login_user(user)
        return redirect (url_for("users.show", id = current_user.id))
    else:
        return '<h1> Failed Login </h1>' 


@sessions_blueprint.route("/logout", methods=["POST"])
@login_required
def destroy():
    logout_user()
    return render_template('home.html')
    # return redirect (url_for("/"))


# @sessions_blueprint.route("/logout", methods=["POST"])
# def update():
#     logout_user()
#     return render_template('home.html')
    # return redirect (url_for("/"))

@sessions_blueprint.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)