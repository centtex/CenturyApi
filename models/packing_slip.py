from . import db


class PackingSlip(db.Model):
    __tablename__ = 'packingslip'

    def __init__(self):
        pass

    sr_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PackingSlipId = db.Column(db.Integer, primary_key=True)
    Baleno = db.Column(db.Integer, nullable=True)
    Lgr_id = db.Column(db.Integer, nullable=True)
    City_Id = db.Column(db.Integer, nullable=True)
    Agent_Id = db.Column(db.Integer, nullable=True)
    Transport_Id = db.Column(db.Integer, nullable=True)
    Station_Id = db.Column(db.Integer, nullable=True)
    Vch_Date = db.Column(db.DateTime, nullable=True)
    ConfNo = db.Column(db.Integer, nullable=True)
    Conf_Date = db.Column(db.DateTime, nullable=True)
    Order_Date = db.Column(db.DateTime, nullable=True)
    OrderNo = db.Column(db.Unicode(255), nullable=True)
    Cmp_Code = db.Column(db.Integer, nullable=True)
    Weight = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Transport_Bill = db.Column(db.Integer, nullable=True)
    Rate_Per = db.Column(db.Float(precision=10, decimal_return_scale=2))
    RukkaNo = db.Column(db.Integer, nullable=True)
    COLOURS = db.Column(db.Unicode(255), nullable=True)
    BalePack_Id = db.Column(db.Integer, nullable=True)
    Series_Id = db.Column(db.Integer, nullable=True)
    JobNo = db.Column(db.Unicode(255), nullable=True)
    Fyear = db.Column(db.Unicode(255), nullable=True)
    LrNo = db.Column(db.Unicode(255), nullable=True)
    SerialNo = db.Column(db.Integer, nullable=True)
    Narration = db.Column(db.Unicode(255), nullable=True)
    Serial_Alias = db.Column(db.Unicode(255), nullable=True)
    PACKED = db.Column(db.Boolean, nullable=True)
    TransportBill_Date = db.Column(db.DateTime, nullable=True)
    SELF_PARTY = db.Column(db.Unicode(255), nullable=True)
    OTHER = db.Column(db.Unicode(255), nullable=True)
    BaleChecker_Id = db.Column(db.Integer, nullable=True)
    ADD_DATE = db.Column(db.DateTime, nullable=True)
    EDIT_DATE = db.Column(db.DateTime, nullable=True)
    USERID = db.Column(db.Integer, nullable=True)
    inuse = db.Column(db.Boolean, nullable=True)
    Godown_Id = db.Column(db.Integer, nullable=True)
    LotNo = db.Column(db.Integer, nullable=True)
    SAMPLE_BALES = db.Column(db.Boolean, nullable=True)
    GIFT_BALES = db.Column(db.Boolean, nullable=True)
    FORMFLAG = db.Column(db.Unicode(255), nullable=True)
    FOLDNO = db.Column(db.Integer, nullable=True)
    FOLD_DATE = db.Column(db.DateTime, nullable=True)
    D_COLNO = db.Column(db.Unicode(255), nullable=True)
    FLAG = db.Column(db.Integer, nullable=True)
    HASTE_ID = db.Column(db.Integer, nullable=True)
    YEAR_FLAG = db.Column(db.Unicode(255), nullable=True)
    REC_TRANS = db.Column(db.Boolean, nullable=True)
    RUKKANO_DATE = db.Column(db.DateTime, nullable=True)
    DISC = db.Column(db.Float(precision=10, decimal_return_scale=2))
    SCHEME = db.Column(db.Float(precision=10, decimal_return_scale=2))
    OrdAssortNo = db.Column(db.Integer, nullable=True)
    AssortFyear = db.Column(db.Unicode(255), nullable=True)


class PackingAssortment(db.Model):
    __tablename__ = 'packingassortment'

    def __init__(self):
        pass

    sr_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PACKINGSLIPID = db.Column(db.Integer, nullable=True)
    SrNo = db.Column(db.Integer, nullable=True)
    ASSORTMENT_ID = db.Column(db.Integer, nullable=True)
    COLNO = db.Column(db.Integer, nullable=True)
    PCS = db.Column(db.Integer, nullable=True)
    CMP_CODE = db.Column(db.Integer, nullable=True)
    RowNo = db.Column(db.Integer, nullable=True)
    FORMFLAG = db.Column(db.Unicode(255), nullable=True)


class PackingSlipDetail(db.Model):
    __tablename__ = 'packingslipdetail'

    def __init__(self):
        pass

    sr_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PackingSlipId = db.Column(db.Integer, nullable=True)
    Srno = db.Column(db.Integer, nullable=True)
    Item_Id = db.Column(db.Integer, nullable=True)
    Item_Cut = db.Column(db.Integer, nullable=True)
    Item_Rate = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Unit_Id = db.Column(db.Integer, nullable=True)
    Screen_Id = db.Column(db.Integer, nullable=True)
    Total = db.Column(db.Float(precision=10, decimal_return_scale=2))
    TotalPcs = db.Column(db.Integer, nullable=True)
    DetailRowNo = db.Column(db.Integer, nullable=True)
    Cmp_Code = db.Column(db.Integer, nullable=True)
    InUse = db.Column(db.Boolean, nullable=True)
    ASSORTMENT_YN = db.Column(db.Unicode(255), nullable=True)
    ASSORTMENT_ID = db.Column(db.Integer, nullable=True)
    TYPE = db.Column(db.Unicode(255), nullable=True)
    CONSIDER = db.Column(db.Unicode(255), nullable=True)
    TotalTp = db.Column(db.Integer, nullable=True)
    Fyear = db.Column(db.Unicode(255), nullable=True)
    EXTRACOL_YN = db.Column(db.Unicode(255), nullable=True)
    COLOR_CHART = db.Column(db.Unicode(255), nullable=True)
    PACKINGSTYLE_ID = db.Column(db.Integer, nullable=True)
    FORMFLAG = db.Column(db.Unicode(255), nullable=True)
    DesignID = db.Column(db.Integer, nullable=True)
    NETMETER = db.Column(db.Float(precision=10, decimal_return_scale=2))


class PackingSlipDetailDetail(db.Model):
    __tablename__ = 'packingslipdetaildetail'

    def __init__(self):
        pass

    SrNo = db.Column(db.Integer, primary_key=True)
    Item_Id = db.Column(db.Integer, nullable=True)
    Pcs = db.Column(db.Integer, nullable=True)
    Mtrs = db.Column(db.Float(precision=10, decimal_return_scale=2))
    Total = db.Column(db.Float(precision=10, decimal_return_scale=2))
    RowNo = db.Column(db.Integer, nullable=True)
    PackingSlipId = db.Column(db.Integer, nullable=True)
    Cmp_Code = db.Column(db.Integer, nullable=True)
    TP = db.Column(db.Integer, nullable=True)
    FORMFLAG = db.Column(db.Unicode(255), nullable=True)
    DesignID = db.Column(db.Integer, nullable=True)
