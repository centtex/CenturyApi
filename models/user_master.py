import flask_bcrypt
from . import db


class UserTypeMaster(db.Model):
    __tablename__ = 'UserTypeMaster'

    def __init__(self, id, type):
        self.id = id
        self.type = type

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), unique=True, nullable=False)


class UserMaster(db.Model):
    __tablename__ = 'UserMaster'

    def __init__(self,
                 user_id, user_name, user_password, user_registered_date, user_update_date, user_type,
                 user_mobile_number, user_email, phone_country_code):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_registered_date = user_registered_date
        self.user_update_date = user_update_date
        self.user_type = user_type
        self.user_mobile_number = user_mobile_number
        self.user_email = user_email
        self.phone_country_code = phone_country_code

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    user_mobile_number = db.Column(db.Unicode(255))
    phone_country_code = db.Column(db.Unicode(8))
    user_registered_date = db.Column(db.DateTime, nullable=False)
    user_update_date = db.Column(db.DateTime, nullable=False)
    user_name = db.Column(db.String(50), unique=True)
    user_password = db.Column(db.String(100))
    user_type = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.user_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
