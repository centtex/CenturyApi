from . import db


class CustomerGroupMaster(db.Model):
    __tablename__ = 'customergrpmaster'

    def __init__(self):
        pass

    Cust_Grp_Id = db.Column(db.Integer, primary_key=True)
    Cust_Grp_Name = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    CR_LIMIT = db.Column(db.Integer, nullable=True)
    # ledger = db.relationship('LedgerMaster', backref='customergrpmaster', lazy=True)


class CourierMaster(db.Model):
    __tablename__ = 'couriermaster'

    def __init__(self):
        pass

    CourierMaster_ID = db.Column(db.Integer, primary_key=True)
    CourierMaster_Name = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    # ledger = db.relationship('LedgerMaster', backref='couriermaster', lazy=True)
    # salesinvoice = db.relationship('SalesInvoice', backref='couriermaster', lazy=True)


class SalesManMaster(db.Model):
    __tablename__ = 'salesmanmaster'

    def __init__(self):
        pass

    SalesMan_ID = db.Column(db.Integer, primary_key=True)
    SalesMan_Name = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    # ledger = db.relationship('LedgerMaster', backref='SalesManMaster', lazy=True)


class LedgerMaster(db.Model):
    __tablename__ = 'ledgermaster'

    def __init__(self):
        pass

    Lgr_Id = db.Column(db.Integer, primary_key=True)
    Lgr_name = db.Column(db.Unicode(255), nullable=True)
    Lgr_Alias = db.Column(db.Unicode(255), nullable=True)
    Lgr_PrintName = db.Column(db.Unicode(255), nullable=True)
    Lgr_Bank = db.Column(db.Unicode(255), nullable=True)
    Lgr_Branch = db.Column(db.Unicode(255), nullable=True)
    Lgr_Post = db.Column(db.Unicode(255), nullable=True)
    Supp_Grp_Id = db.Column(db.Integer, nullable=True)
    Category_Id = db.Column(db.Integer, nullable=True)  # not to consider, will refer from usermaster
    Gen_Grp_Id = db.Column(db.Integer, nullable=True)
    Lgr_Commition = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_InterestRate = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Cr_Period_day = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Cr_Limit = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Add1 = db.Column(db.Unicode(255), nullable=True)
    Lgr_Add2 = db.Column(db.Unicode(255), nullable=True)
    Lgr_Add3 = db.Column(db.Unicode(255), nullable=True)
    Lgr_Phone1 = db.Column(db.Unicode(255), nullable=True)
    Lgr_Phone2 = db.Column(db.Unicode(255), nullable=True)
    Lgr_Mobile = db.Column(db.Unicode(255), nullable=True)
    Lgr_Fax = db.Column(db.Unicode(255), nullable=True)
    Lgr_Email = db.Column(db.Unicode(255), nullable=True)
    Lgr_WebSite = db.Column(db.Unicode(255), nullable=True)
    Lgr_Cont_Person = db.Column(db.String(100), nullable=True)
    Lgr_Pano = db.Column(db.String(10), nullable=True)
    Lgr_Cstno = db.Column(db.Unicode(255), nullable=True)
    Lgr_Stno = db.Column(db.Unicode(255), nullable=True)
    Lgr_TDSNo = db.Column(db.Unicode(255), nullable=True)
    Lgr_Type = db.Column(db.Unicode(255), nullable=True)
    Lgr_Station_Id = db.Column(db.Integer, nullable=True)
    TdsApp = db.Column(db.Unicode(255), nullable=True)
    Deductee_Code = db.Column(db.Integer, nullable=True)
    TdsNature_Code = db.Column(db.Integer, nullable=True)
    TdsNatureAcId = db.Column(db.Integer, nullable=True)
    Lgr_District = db.Column(db.Unicode(255), nullable=True)
    City_PinCode = db.Column(db.Unicode(255), nullable=True)
    LGR_STOP = db.Column(db.Boolean, nullable=True)
    BF1stHALF = db.Column(db.Integer, nullable=True)
    AF1stHALF = db.Column(db.Integer, nullable=True)
    OPNG_DEP_PER = db.Column(db.Integer, nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    Lgr_Cash_Disc = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    Sal_DiscPer = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    Sal_Reb_Per = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    Brok_Per = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    Sal_Insurance = db.Column(db.Boolean, nullable=True)
    Sal_Reb_Less = db.Column(db.Boolean, nullable=True)
    INSURANCE_PER = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    INSURANCE_STOP = db.Column(db.Boolean, nullable=True)
    InterestType = db.Column(db.Unicode(255), nullable=True)
    Lgr_IFSCCODE1 = db.Column(db.Unicode(255), nullable=True)
    Lgr_IFSCCODE2 = db.Column(db.Unicode(255), nullable=True)
    Lgr_IFSCCODE3 = db.Column(db.Unicode(255), nullable=True)
    Lgr_BankAccNo1 = db.Column(db.Unicode(255), nullable=True)
    Lgr_BankAccNo2 = db.Column(db.Unicode(255), nullable=True)
    Lgr_BankAccNo3 = db.Column(db.Unicode(255), nullable=True)
    LGR_AdvanceEntry = db.Column(db.Boolean, nullable=True)
    ADVANCE_DIS_PER = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    RISK = db.Column(db.Boolean, nullable=True)
    LGR_DAYSLIMIT = db.Column(db.Integer, nullable=True)
    GSTINNO = db.Column(db.Unicode(255), nullable=True)
    ADHARNO = db.Column(db.Unicode(255), nullable=True)
    Register_Dealer_Type = db.Column(db.Unicode(255), nullable=True)
    Supply_Type = db.Column(db.Unicode(255), nullable=True)
    Gst_Supply_Type = db.Column(db.Unicode(255), nullable=True)
    IECODE = db.Column(db.Unicode(255), nullable=True)
    CashDiscInBill = db.Column(db.Float(precision=10, decimal_return_scale=2), nullable=False)
    EwayUserId = db.Column(db.Unicode(255), nullable=True)
    EwayPassword = db.Column(db.Unicode(255), nullable=True)
    PAYMENT_TYPE = db.Column(db.Unicode(255), nullable=True)
    No_LessAmt = db.Column(db.Boolean, nullable=True)
    JobStatus = db.Column(db.Unicode(255), nullable=True)
    BENEFICIARYCODE = db.Column(db.Unicode(255), nullable=True)
    EMP_CODE = db.Column(db.Unicode(255), nullable=True)
    Lgr_WhatsappMobile = db.Column(db.Unicode(255), nullable=True)
    EXPORTBANK_ID = db.Column(db.Unicode(255), nullable=True)

    USERID = db.Column(db.Integer, nullable=True)
    SalesMan_Id = db.Column(db.Integer, nullable=True)
    CourierMaster_Id = db.Column(db.Integer, nullable=True)
    Cust_Grp_Id = db.Column(db.Integer, nullable=True)
    COUNTRY_ID = db.Column(db.Integer, nullable=True)
    State_Id = db.Column(db.Integer, nullable=True)
    City_Id = db.Column(db.Integer, nullable=True)

    # adj = db.relationship('ADJMaster', backref='ledgermaster', lazy=True)
    # transport = db.relationship('TransportMaster', backref='ledgermaster', lazy=True)
    # ledgerdetail = db.relationship('LedgerDetail', backref='ledgermaster', lazy=True)
    # salesorder = db.relationship('SalesOrder', backref='ledgermaster', lazy=True)
    # salesinvoice = db.relationship('SalesInvoice', backref='ledgermaster', lazy=True)
    # salesinvoiceconfig = db.relationship('SalesInvoiceConfig', backref='ledgermaster', lazy=True)
    # packingslip = db.relationship('PackingSlip', backref='ledgermaster', lazy=True)
    # partydetail = db.relationship('PartyDetail', backref='ledgermaster', lazy=True)



    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {


        }


class LedgerDetail(db.Model):
    __tablename__ = 'ledgerdetail'

    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Lgr_Id = db.Column(db.Integer, nullable=True)
    cmp_code = db.Column(db.Integer, nullable=True)
    grp_Id = db.Column(db.Integer, nullable=True)
    Agent_Id = db.Column(db.Integer, nullable=True)
    Transport_Id = db.Column(db.Integer, nullable=True)
    Lgr_Op_Bal = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Op_DrCr = db.Column(db.Unicode(255), nullable=True)
    Lgr_Cl_Bal = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Cl_DrCr = db.Column(db.Unicode(255), nullable=True)
    Lgr_Total_Cr_Bal = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Lgr_Total_Dr_Bal = db.Column(db.Float(precision=10, decimal_return_scale=2))
    ACCOUNT_ID = db.Column(db.Integer, nullable=True)
    PAYEE_ID = db.Column(db.Integer, nullable=True)
    TDS_ID = db.Column(db.Integer, nullable=True)
    TDSOnBill = db.Column(db.Unicode(255), nullable=True)
    TDSRate = db.Column(db.Float(precision=10, decimal_return_scale=2))
    TDS_B4LR_CERTI = db.Column(db.Float(precision=10, decimal_return_scale=2))
    DATE_LRCERTI = db.Column(db.Float(precision=10, decimal_return_scale=2))
    TDS_PER_ALRCERTI_EXC = db.Column(db.Float(precision=10, decimal_return_scale=2))
    TDS_LMT_LRCERTI = db.Column(db.Float(precision=10, decimal_return_scale=2))
    TDSAllBill = db.Column(db.Unicode(255), nullable=True)
