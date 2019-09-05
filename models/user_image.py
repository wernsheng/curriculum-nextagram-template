from models.base_model import BaseModel
from models.user import User
import peewee as pw
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property
import os
import boto3, botocore

class User_image(BaseModel, UserMixin): #To make implementing a user class easier, you can inherit from UserMixin, which provides default implementations for all of these properties and methods. (It’s not required, though.)
    user = pw.ForeignKeyField(User, backref='images')
    user_image = pw.CharField(null=True)

    @hybrid_property
    def user_image_url(self):
        from app import s3, S3_BUCKET # import function has been pushed down here as app.py refers to user.py to access User which in turn called on App to pull s3. In order to avoid circular reference.
        if self.user_image:
            return f'https://{S3_BUCKET}.s3-ap-southeast-1.amazonaws.com/' + self.user_image
        else:
            return f'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAGFBMVEXx7/D////18/T6+vr49/j08vP8/Pzw7e+uV6dtAAABfUlEQVR4nO3ayXKCUBBAUeXB4///OCEGmVQMLKx0n7NTYNG3mIvLBQAAAAAAAAAAAAAAAAAAAACANLrmrO7TI5xWr2eVT49wmgYaDDS4NWj6gxv3bZwGh7fWQINBrAbtn8+F41YaaKBB5Aa16bpm9+YpdIPfy0SXuMH4LNzvRAjcoJ2WvT5HBG4wX6jBzkNl3AZ1vTBhA8fCdbosDOYjb/aJwA1mI5XFyOsIgRtMF8dmMfLqZ+wGQ4S+X98dlM0ZMnSD77Hatlw3EzebfyI3eGBcN3GDn0GXO0K6Bs195bwNbisvdoRsDcY76MwNxrfvZfVfpgbj2vPXKskaTA+TWRuU2WPU7GDI06AsP7Xp0jUo22+NcjV4EOAyPxjiN3g2WZenwfPB0jR4MVdJ0uDVWF2OBq+nqhka7A1V4zfYn6lGb/DOSDVmg/v3629tNa4Yq8ExGmgwiNOgtEfVMA3O0UCDGA3actbxMyoAAAAAAAAAAAAAAAAAAAAAAPxDX+w9D05sn3cWAAAAAElFTkSuQmCC'

