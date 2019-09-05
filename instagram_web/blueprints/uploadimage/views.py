import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from models.user_image import User_image
from flask_login import login_user, current_user, login_required
import boto3, botocore
from app import s3, S3_BUCKET, upload_file_to_s3

uploadimage_blueprint = Blueprint('uploadimage',
                            __name__,
                            template_folder='templates')


@uploadimage_blueprint.route('/<id>', methods=['GET'])
def new(id):
    return render_template('uploadimage/upload_image.html')

# Upload profile photo
@uploadimage_blueprint.route('/<id>/done', methods=['POST'])
def update(id):
    # user = User.get_by_id(id) # the user we are modifying, based on id from form action
    # user_image = User_image.get_or_none(User_image.user_id == id)
    user_picture = request.files.get('user_picture')
    if upload_file_to_s3(user_picture):
        user_image = User_image (user_id = current_user.id, user_image = user_picture.filename)
        if user_image.save():
            flash("Successfully uploaded")
        # current_user ==  user: # current_user method is from Flask-Login
        # User_image.update(user_image=user_picture.filename).where(User_image.user_id == id).execute()
            return render_template('uploadimage/upload_image.html')
        else:
            return '<h1> You do not have sufficient permission </h1>'
