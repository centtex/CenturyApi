from . import db


class UnitMaster(db.Model):
    __tablename__ = 'unitmaster'

    def __init__(self):
        pass

    Unit_Id = db.Column(db.Integer, primary_key=True)
    Unit_Name = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    UQC = db.Column(db.Unicode(255), nullable=True)
    UNIT_CODE = db.Column(db.Unicode(255), nullable=True)
    # item = db.relationship('itemmaster', backref='unitmaster', lazy=True)
    # packingslipdetail = db.relationship('PackingSlipDetail', backref='unitmaster', lazy=True)


class HSNMaster(db.Model):
    __tablename__ = 'hsnmaster'

    def __init__(self):
        pass

    Hsn_Id = db.Column(db.Integer, primary_key=True)
    Hsn_Name = db.Column(db.Unicode(255), nullable=True)
    Description = db.Column(db.Unicode(255), nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    CGST = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SGST = db.Column(db.Float(precision=10, decimal_return_scale=2))
    IGST = db.Column(db.Float(precision=10, decimal_return_scale=2))
    GST_TYPE = db.Column(db.Unicode(255), nullable=True)
    # item = db.relationship('ItemMaster', backref='hsnmaster', lazy=True)


class ItemGroupMaster(db.Model):
    __tablename__ = 'itemgrpmaster'

    def __init__(self):
        pass

    Item_Grp_Id = db.Column(db.Integer, primary_key=True)
    Item_Grp_Name = db.Column(db.Unicode(255), nullable=True)
    Item_Grp_Weight = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_Grp_Godown = db.Column(db.Float(precision=10, decimal_return_scale=2))
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    SERIALNO = db.Column(db.Float(precision=10, decimal_return_scale=2))
    # item = db.relationship('ItemMaster', backref='itemgrpmaster', lazy=True)


class ItemMaster(db.Model):
    __tablename__ = 'itemmaster'

    def __init__(self):
        pass

    Item_Id = db.Column(db.Integer, primary_key=True)
    Item_Name = db.Column(db.Unicode(255), nullable=True)
    Unit_Id = db.Column(db.Integer, nullable=True)
    Item_Grp_Id = db.Column(db.Integer, nullable=True)
    Item_Type = db.Column(db.Unicode(255), nullable=True)
    Item_Conversion = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_Cut = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_Reads = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_Peak = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_GWidth = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_GWeight = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Item_DWeight = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Rate_Per = db.Column(db.Unicode(255), nullable=True)
    Item_Goods_Type = db.Column(db.Unicode(255), nullable=True)
    Item_type_Id = db.Column(db.Integer, nullable=True)
    Item_Weight = db.Column(db.Float(precision=10, decimal_return_scale=2))
    ADD_DATE = db.Column(db.DateTime, nullable=False)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    SCHEME_PER = db.Column(db.Float(precision=10, decimal_return_scale=2))
    LOT_ID = db.Column(db.Float(precision=10, decimal_return_scale=2))
    NOLESS = db.Column(db.Boolean, nullable=True)
    HSN_ID = db.Column(db.Integer, nullable=True)
    # packingslipdetail = db.relationship('PackingSlipDetail', backref='itemmaster', lazy=True)
    # packingslipdetaildetail = db.relationship('PackingSlipDetailDetail', backref='itemmaster', lazy=True)
    # salesinvoicedetail = db.relationship('SalesInvoiceDetail', backref='dbo.itemmaster', lazy=True)
    # salesorderdetail = db.relationship('SalesInvoiceDetail', backref='dbo.itemmaster', lazy=True)
