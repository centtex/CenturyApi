import flask_bcrypt
from . import db


# from sqlalchemy_utils import PhoneNumber
class UserTypeMaster(db.Model):
    __tablename__ = 'usertypemaster'

    def __init__(self, _id, _type):
        self.id = _id
        self.type = _type

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), unique=True, nullable=False)

    # user = db.relationship('UserMaster', lazy=True, backref='UserTypeMaster',
    #                        primaryjoin="UserMaster.user_type == UserTypeMaster.id")

    def __repr__(self):
        return "<UserType '{}'>".format(self.type)


class UserMaster(db.Model):
    __tablename__ = 'usermaster'

    def __init__(self,
                 _user_id, _user_name, _user_password, _user_registered_date, _user_update_date, _user_type,
                 _user_mobile_number, _user_email, _phone_country_code, _lgr_id):
        self.user_id = _user_id
        self.user_name = _user_name
        self.user_password = _user_password
        self.user_registered_date = _user_registered_date
        self.user_update_date = _user_update_date
        self.user_type = _user_type
        self.user_mobile_number = _user_mobile_number
        self.user_email = _user_email
        self.phone_country_code = _phone_country_code
        self.lgr_id = _lgr_id

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.Unicode(255), nullable=True)
    user_mobile_number = db.Column(db.Unicode(255), index=True, nullable=True)
    phone_country_code = db.Column(db.Unicode(8), nullable=False)
    user_registered_date = db.Column(db.DateTime, nullable=False)
    user_update_date = db.Column(db.DateTime, nullable=True)
    lgr_id = db.Column(db.Integer, nullable=True)
    user_password = db.Column(db.String(100))
    user_token = db.Column(db.Unicode(255))
    user_type = db.Column(db.Integer, nullable=True)
    isActive = db.Column(db.Boolean, nullable=True)



    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'user_id': self.user_id,
            'user_password': self.user_password,
            'user_registered_date': self.user_registered_date,
            'user_update_date': self.user_update_date,
            'user_type': self.user_type,
            'user_mobile_number': self.user_mobile_number,
            'user_email': self.user_email,
            'phone_country_code': self.phone_country_code,
            'lgr_id': self.lgr_id,
            'id': self.user_id
        }

        # ledger = db.relationship('LedgerMaster', lazy=True)
        # customer_grp = db.relationship('CustomerGrpMaster', lazy=True)
        # courier = db.relationship('CourierMaster', lazy=True)
        # item = db.relationship('ItemMaster', lazy=True)
        # salesorder = db.relationship('SalesOrder', lazy=True)
        # partydetail = db.relationship('PartyDetail', lazy=True)
        # unitmaster = db.relationship('UnitMaster', lazy=True)
        # hsnmaster = db.relationship('HSNMaster', lazy=True)
        # itemgroupmaster = db.relationship('ItemGroupMaster', lazy=True)
        # salesmanmaster = db.relationship('SalesmanMaster', lazy=True)
        # packingslip = db.relationship('PackingSlip', lazy=True)
        # hastemaster = db.relationship('HasteMaster', lazy=True)
        # transportmaster = db.relationship('TransportMaster', lazy=True)
        # screenmaster = db.relationship('ScreenMaster', lazy=True)

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
