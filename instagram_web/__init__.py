from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.uploadimage.views import uploadimage_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
import os
from instagram_web.helpers.google_oauth import oauth
import config


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/")
app.register_blueprint(uploadimage_blueprint, url_prefix="/uploadimage")

oauth.init_app(app)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('home.html') #  user=User.get_by_id(30)

    
