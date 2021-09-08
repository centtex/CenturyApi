from . import db


class TransportMaster(db.Model):
    __tablename__ = 'transportmaster'

    def __init__(self):
        pass

    Transport_Id = db.Column(db.Integer, primary_key=True)
    Transport_Name = db.Column(db.Unicode(255), nullable=True)
    Lgr_ID = db.Column(db.Integer, db.ForeignKey('ledgermaster.Lgr_Id'))
    TRANS_ADD1 = db.Column(db.Unicode(255), nullable=True)
    TRANS_ADD2 = db.Column(db.Unicode(255), nullable=True)
    TRANS_ADD3 = db.Column(db.Unicode(255), nullable=True)
    DISTRICT = db.Column(db.Unicode(255), nullable=True)
    STATE_ID = db.Column(db.Integer, db.ForeignKey('statemaster.state_id'))
    CITY_ID = db.Column(db.Integer, db.ForeignKey('citymaster.city_id'))
    PINCODE = db.Column(db.Unicode(255), nullable=True)
    PHONE1 = db.Column(db.Unicode(255), nullable=True)
    PHONE2 = db.Column(db.Unicode(255), nullable=True)
    MOBILE = db.Column(db.Unicode(255), nullable=True)
    FAX = db.Column(db.Unicode(255), nullable=True)
    EMAIL = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, db.ForeignKey('usermaster.user_id'))
    TNAME = db.Column(db.Unicode(255), nullable=True)
    TMODE = db.Column(db.Unicode(255), nullable=True)
    TRANSEW_ID = db.Column(db.Unicode(255), nullable=True)
    TTYPE = db.Column(db.Unicode(255), nullable=True)

    # ledgerdetail = db.relationship('LedgerDetail', backref='transportmaster', lazy=True)
    # salesorder = db.relationship('SalesOrder', backref='transportmaster', lazy=True)
    # salesinvoice = db.relationship('SalesInvoice', backref='transportmaster', lazy=True)
    # packingslip = db.relationship('PackingSlip', backref='transportmaster', lazy=True)
    # partydetail = db.relationship('PartyDetail', backref='transportmaster', lazy=True)


class ScreenMaster(db.Model):
    __tablename__ = 'screenmaster'

    def __init__(self):
        pass

    Screen_ID = db.Column(db.Integer, primary_key=True)
    Screen_Name = db.Column(db.Unicode(255), nullable=True)
    Item_Id = db.Column(db.Integer, nullable=True)
    Scheme = db.Column(db.Unicode(255), nullable=True)
    Incentive = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    SCREEN_STOP = db.Column(db.Boolean, nullable=True)
    TRADEMARK_ID = db.Column(db.Integer, nullable=True)
    # packingslipdetail = db.relationship('PackingSlipDetail', backref='screenmaster', lazy=True)
    # salesorderdetail = db.relationship('SalesOrderDetail', backref='screenmaster', lazy=True)
