from . import db


class CountryMaster(db.Model):
    __tablename__ = 'countrymaster'

    def __init__(self, country_id, country_name, country_code, add_date, edit_date):
        self.country_id = country_id
        self.country_name = country_name
        self.country_code = country_code
        self.add_date = add_date
        self.edit_date = edit_date

    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_name = db.Column(db.String(50), unique=True, nullable=False)
    country_code = db.Column(db.String(4), unique=True, nullable=False)
    add_date = db.Column(db.DateTime, nullable=False)
    edit_date = db.Column(db.DateTime, nullable=False)
    # country = db.relationship('StateMaster', backref = 'countrymaster', lazy = True)


class StateMaster(db.Model):
    __tablename__ = 'statemaster'

    def __init__(self, state_id, state_name, state_code, in_outer_state, add_date, edit_date):
        self.state_id = state_id
        self.state_name = state_name
        self.state_code = state_code
        self.in_outer_state = in_outer_state
        self.add_date = add_date
        self.edit_date = edit_date

    state_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(50), unique=True, nullable=False)
    state_code = db.Column(db.String(4), unique=True, nullable=False)
    in_outer_state = db.Column(db.String(40), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country_id'))
    add_date = db.Column(db.DateTime, nullable=False)
    edit_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    # state = db.relationship('CityMaster', backref = 'statemaster', lazy = True)


class CityMaster(db.Model):
    __tablename__ = 'citymaster'

    def __init__(self, city_id, city_name, city_district, city_pincode, state_id, add_date, edit_date, city_code,
                 distance):
        self.city_id = city_id
        self.city_name = city_name
        self.city_district = city_district
        self.city_pincode = city_pincode
        self.city_code = city_code
        self.state_id = state_id
        self.add_date = add_date
        self.edit_date = edit_date
        self.distance = distance

    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(50), unique=True, nullable=False)
    city_district = db.Column(db.String(4), unique=True, nullable=False)
    city_pincode = db.Column(db.String(40), unique=True, nullable=False)
    city_code = db.Column(db.String(4), unique=True, nullable=False)
    add_date = db.Column(db.DateTime, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state_id'))
    edit_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Float(precision=10, decimal_return_scale=2))
