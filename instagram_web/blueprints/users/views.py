from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_password = request.form['user_password']
    hashed_password = generate_password_hash(password)
    user = User (name = request.form['name'], username = request.form['username'], email = request.form['email'], password = request.form['password'])
    if user.save():
        flash("Successfully saved")
        return redirect (url_for('/<username>'))
    else: 
        return render_template ('new.html')

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

