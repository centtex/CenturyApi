from . import db


class ADJMaster(db.Model):
    __tablename__ = 'adjmaster'

    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SrNo = db.Column(db.Integer, primary_key=False)
    EntryCode = db.Column(db.Integer, nullable=True)
    Vcode = db.Column(db.Integer, nullable=True)
    Lgr_Id = db.Column(db.Integer, nullable=True)
    BillNo = db.Column(db.Unicode(255), nullable=True)
    Type = db.Column(db.Unicode(255), nullable=True)
    Flag = db.Column(db.Unicode(255), nullable=True)
    Date = db.Column(db.DateTime, nullable=False)
    RecDate = db.Column(db.DateTime, nullable=False)
    CHEQUENO = db.Column(db.Unicode(255), nullable=True)
    ChequeDate = db.Column(db.DateTime, nullable=False)
    Amount = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Disc_Per = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Discount = db.Column(db.Float(precision=10, decimal_return_scale=2))
    OtherLess = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Total = db.Column(db.Float(precision=10, decimal_return_scale=2))
    AdjustAmt = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Interest = db.Column(db.Float(precision=10, decimal_return_scale=2))
    IntRec = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Paid = db.Column(db.Boolean, nullable=True)
    Cmp_Code = db.Column(db.Integer, nullable=True)
    Remark = db.Column(db.Integer, nullable=True)
    RECEIPT_ID = db.Column(db.Integer, nullable=True)
    SAL_INSURANCEAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SAL_RATEDIFFAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SAL_REB_PER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SAL_REBAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SCHEMEAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    INT_PER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    OTHER_PER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    OTHER_PERAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    OTHER_DISC = db.Column(db.Float(precision=10, decimal_return_scale=2))
    BROK_PER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    BROK_PERAMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    DEBIT_AMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    CREDIT_AMT = db.Column(db.Float(precision=10, decimal_return_scale=2))
    ADJ_OTHER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    ADJ_INTEREST = db.Column(db.Float(precision=10, decimal_return_scale=2))
