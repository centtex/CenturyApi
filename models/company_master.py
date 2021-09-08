from . import db


class CompanyMaster(db.Model):
    __tablename__ = 'companymaster'

    def __init__(self):
        pass

    cmp_Code = db.Column(db.Integer, primary_key=True)
    cmp_Name = db.Column(db.Unicode(255), nullable=False)
    cmp_Tin_No = db.Column(db.Unicode(255), nullable=False)
    cmp_ServiceTax_No = db.Column(db.Unicode(255), nullable=False)
    cmp_Tds_No = db.Column(db.Unicode(255), nullable=False)
    cmp_Pan_No = db.Column(db.Unicode(255), nullable=False)
    cmp_Alias = db.Column(db.Unicode(255), nullable=False)
    cmp_Inv_Hading = db.Column(db.Integer, nullable=True)
    cmp_Item_Hading = db.Column(db.Integer, nullable=True)
    cmp_Specification = db.Column(db.Integer, nullable=True)
    cmp_Registration_No = db.Column(db.Integer, nullable=True)
    cmp_Jurisdiction = db.Column(db.Unicode(255), nullable=False)
    cmp_InterestRate = db.Column(db.Float, nullable=True)
    cmp_Contact_Person = db.Column(db.Unicode(255), nullable=False)
    cmp_Add1 = db.Column(db.Unicode(255), nullable=False)
    cmp_Add2 = db.Column(db.Unicode(255), nullable=False)
    cmp_City = db.Column(db.Unicode(255), nullable=False)
    cmp_Pincode = db.Column(db.Unicode(255), nullable=False)
    cmp_State = db.Column(db.Unicode(255), nullable=False)
    cmp_Phone1 = db.Column(db.Unicode(255), nullable=False)
    cmp_Phone2 = db.Column(db.Unicode(255), nullable=False)
    cmp_Mobile = db.Column(db.Unicode(255), nullable=False)
    cmp_Fax = db.Column(db.Unicode(255), nullable=False)
    cmp_Email = db.Column(db.Unicode(255), nullable=False)
    cmp_Web = db.Column(db.Unicode(255), nullable=False)
    cmp_Fc_Add1 = db.Column(db.Unicode(255), nullable=False)
    cmp_Fc_Add2 = db.Column(db.Unicode(255), nullable=False)
    cmp_Fc_City = db.Column(db.Unicode(255), nullable=False)
    cmp_Fc_Pincode = db.Column(db.Unicode(255), nullable=False)
    cmp_Fc_State = db.Column(db.Unicode(255), nullable=False)
    cmp_Bank_Accno1 = db.Column(db.Unicode(255), nullable=False)
    cmp_Bank_Accno2 = db.Column(db.Unicode(255), nullable=False)
    cmp_Bank_Accno3 = db.Column(db.Unicode(255), nullable=False)
    cmp_Round_Off = db.Column(db.Float, nullable=True)
    cmp_StartYear = db.Column(db.DateTime, nullable=False)
    cmp_EndYear = db.Column(db.DateTime, nullable=False)
    cmp_TdsApp = db.Column(db.Boolean, nullable=True)
    cmp_TdsLmt = db.Column(db.Float, nullable=True)
    cmp_S_Bill_Lmt = db.Column(db.Float, nullable=True)
    Deducted_Type = db.Column(db.Unicode(255), nullable=False)
    GSTINNO = db.Column(db.Unicode(255), nullable=False)
    cmpStateCode = db.Column(db.Integer, nullable=True)
    BINNO = db.Column(db.Unicode(255), nullable=False)
    IECNO = db.Column(db.Unicode(255), nullable=False)

    # ledgerdetail = db.relationship('LedgerDetail', backref='companymaster', lazy='True')
    # salesorder = db.relationship('SalesOrder', backref='companymaster', lazy='True')
    # salesorderdetail = db.relationship('SalesOrderDetail', backref='companymaster', lazy='True')
    # salesinvoice = db.relationship('SalesInvoice', backref='companymaster', lazy='True')
    # packingslipdetail = db.relationship('PackingSlipDetail', backref='companymaster', lazy=True)
    # packingslipdetaildetail = db.relationship('PackingSlipDetailDetail', backref='companymaster', lazy=True)
    # partydetail = db.relationship('PartyDetail', backref='companymaster', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
