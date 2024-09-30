"""
This file contains the User class which is used to create a user object.
"""

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
