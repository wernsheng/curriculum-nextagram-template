import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from models.user_image import User_image
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, login_required
import boto3, botocore
from app import s3, S3_BUCKET, upload_file_to_s3


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['user_password']
    hashed_password = generate_password_hash(user_password)
    user = User (name = request.form['name'], username = request.form['username'], email = request.form['email'], password = hashed_password)
    if user.save():
        flash("Successfully saved")
        login_user(user)
        # return redirect ("/")
        return redirect (url_for("users.show" , id = current_user.id ))
    else: 
        return render_template ('new.html')


# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"

# Render update details page
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    if current_user ==  user: # current_user method is from Flask-Login
        return render_template('users/edit.html')
    else:
        return '<h1> You do not have sufficient permission </h1>'

# Update username
@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    updated_username = request.form['updated_username']
    if current_user ==  user: # current_user method is from Flask-Login
        User.update(username=updated_username).where(User.id == id).execute()
        return redirect (url_for("users.show" , id = current_user.id))
    else:
        return '<h1> You do not have sufficient permission </h1>'

# Render profile picture page
@users_blueprint.route('/<id>/upload', methods=['GET'])
@login_required
def edit_photo(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    if current_user ==  user: # current_user method is from Flask-Login
        return render_template('users/upload.html')
    else:
        return '<h1> You do not have sufficient permission </h1>'


# Upload profile photo
@users_blueprint.route('/<id>/uploaded', methods=['POST'])
def update_photo(id):
    user = User.get_by_id(id) # the user we are modifying, based on id from form action
    profile_picture = request.files.get('profile_picture')
    # file = request.form['profile_picture']
    if current_user ==  user: # current_user method is from Flask-Login
        upload_file_to_s3(profile_picture)
        User.update(profile_pic=profile_picture.filename).where(User.id == id).execute()
        return render_template('users/upload.html')
    else:
        return '<h1> You do not have sufficient permission </h1>'


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    user = User.get_by_id(id)
    return render_template('users/profile.html', user=user)


@users_blueprint.route('/profiles', methods=["GET"])
def show_profiles():
    users = User.select().prefetch(User_image)
    # user = User.get_or_none(User.username == username)
    return render_template('users/other_profiles.html', users=users)