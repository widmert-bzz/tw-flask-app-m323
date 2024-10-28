from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from user_dao import UserDao
import bcrypt

user_blueprint = Blueprint('user_blueprint', __name__)
user_dao = UserDao('todo_example.db')


@user_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.form
    user = user_dao.get_user_by_username(data['username'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
        login_user(user)
        return redirect(url_for('todo_blueprint.get_all_todos'))
    return jsonify({'error': 'Invalid username or password'}), 401


@user_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_blueprint.login_page'))
