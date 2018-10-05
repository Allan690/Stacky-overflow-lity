import os
from flask import request, jsonify, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from .models import User

user_object = User()
auth = Blueprint('v1_user', __name__)


def login_token_required(f):

    """All endpoints requiring login will be wrapped using this decorator"""
    @wraps(f)
    def decorate_login(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"Message": "You're not logged in. Please login"}), 401

        try:
            details = jwt.decode(token, os.getenv('SECRET'))
            if details['username'] in user_object.u_token:
                curr_user = user_object.users[details['username']]
            else:
                return jsonify({"Message": "Your token is expired, please login again "}), 401
        except BaseException:
            return jsonify({'Message': 'Your request is invalid'}), 401

        return f(curr_user, *args, **kwargs)

    return decorate_login()


@auth.route('/register', methods=['POST'])
def create_user():
    """This method receives user input in JSON format and generates password hash for
    the password parameter"""
    user_input = request.get_json()
    password_hash = generate_password_hash(user_input['password'], method='sha256')
    if user_input['username'] in user_object.users:
        return jsonify({'Message': "This user already exists"}), 400
    if user_input['username'] == "" or user_input['password'] == "":
        return jsonify({'Message':
                        "Your user name and password are required"}), 400
    if not isinstance(user_input['username'], str):
        return jsonify({"Message":
                        "Invalid username. Please enter a valid username"}), 400
    user_input = user_object.create_user(user_input['username'], password_hash)
    return jsonify({"Message": "User registered successfully"}), 201


@auth.route('/login', methods=['POST'])
def login_user():
    """This method allows a user to login and generate an authentication token"""
    auth = request.get_json()

    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"Message": "login required!"}), 401

    if auth['username'] not in user_object.users.keys():
        return jsonify({"Message": "Username not found!"}), 401

    user = user_object.users[auth['username']]
    if check_password_hash(user['password'], auth['password']):
        session['user_logged_in'] = True
        session['user_name'] = auth['username']
        token = jwt.encode({'username': user['username'],
                            'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=20)},
                           os.getenv('SECRET'))
        user_object.user_token[user['username']] = token
        return jsonify({"token": token.decode('UTF-8')}), 200

    return jsonify({"Message": "This login is invalid!"}), 401


@auth.route('/logout', methods=['DELETE'])
@login_token_required
def logout_user(current_user):
    """This method destroys the current user's session"""
    if session and session['user_logged_in']:
        session.clear()
        return jsonify({"Message": "User logged out successfully!"}), 200
    return jsonify({"Message": "User is already logged out"}), 400


@auth.route('/reset-password', methods=['PUT'])
@login_token_required
def reset_user_password(current_user):
    """
    This method requires the user to login before updating their password
    """
    user_input = request.get_json()
    password_hash = generate_password_hash(user_input['password'], method='sha256')
    usr = user_object.users[current_user["username"]]
    usr.update({"password": password_hash})
    return jsonify({"Message": "User password has been reset"}), 202

