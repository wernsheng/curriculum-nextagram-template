from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
import os
import boto3, botocore



class User(BaseModel, UserMixin): #To make implementing a user class easier, you can inherit from UserMixin, which provides default implementations for all of these properties and methods. (It’s not required, though.)
    name = pw.CharField(unique=False)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    username = pw.CharField(unique=True)
    profile_pic = pw.CharField(null=True)

    @hybrid_property
    def profile_image_url(self):
        from app import s3, S3_BUCKET # import function has been pushed down here as app.py refers to user.py to access User which in turn called on App to pull s3. In order to avoid circular reference.
        if self.profile_pic:
            return f'https://{S3_BUCKET}.s3-ap-southeast-1.amazonaws.com/' + self.profile_pic
        else:
            return f'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'
            
