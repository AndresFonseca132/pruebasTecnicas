from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, ID, name, last_name, email, password, document, super_user) -> None:
        self.ID = ID
        self.name = name
        self.last_name = last_name
        self.email = email
        self.document = document
        self.password = password
        self.super_user = super_user

    def get_id(self):
        return str(self.ID)

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

