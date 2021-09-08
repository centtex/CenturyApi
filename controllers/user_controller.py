from models import db, user_master, ledger_master
from models.address_master import StateMaster, CityMaster
from flask import jsonify, request
from sqlalchemy import func
import re


class UserController:

    def index(self):
        return "UserApi"

    def getuser(self, user_id):
        user_data = None
        try:
            user_id = int(user_id)
        except:
            pass
        if user_id and type(user_id) is int:
            if len(str(user_id)) == 10 and user_id != 9999999999:
                user_data = db.session.query(user_master.UserMaster.user_mobile_number.label("mobile"),
                                             user_master.UserMaster.user_type.label("type"),
                                             ledger_master.LedgerMaster.Lgr_Id.label("id"),
                                             ledger_master.LedgerMaster.Lgr_Email.label("email"),
                                             ledger_master.LedgerMaster.Lgr_name.label("name"),
                                             ledger_master.LedgerMaster.Lgr_Add1,
                                             ledger_master.LedgerMaster.Lgr_Add2,
                                             ledger_master.LedgerMaster.Lgr_Add3,
                                             ledger_master.LedgerMaster.City_PinCode,
                                             CityMaster.city_name,
                                             StateMaster.state_name,
                                             ledger_master.LedgerMaster.GSTINNO.label("GSTINNO"),
                                             ) \
                    .join(ledger_master.LedgerMaster,
                          user_master.UserMaster.lgr_id == ledger_master.LedgerMaster.Lgr_Id) \
                    .join(StateMaster, ledger_master.LedgerMaster.State_Id == StateMaster.state_id, isouter=True) \
                    .join(CityMaster, ledger_master.LedgerMaster.City_Id == CityMaster.city_id, isouter=True) \
                    .filter(user_master.UserMaster.user_mobile_number == int(user_id),
                            user_master.UserMaster.isActive == 1) \
                    .all()
                # user_data = db.session.query(user_master.UserMaster) \
                #     .join(ledger_master.LedgerMaster,
                #           user_master.UserMaster.lgr_id == ledger_master.LedgerMaster.Lgr_Id) \
                #     .filter(user_master.UserMaster.user_mobile_number == int(user_id)).all()
                print(len(user_data))
            else:
                return "Invalid mobile Number"
        else:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if re.match(regex, user_id):
                user_data = db.session.query(user_master.UserMaster.user_mobile_number.label("mobile"),
                                             user_master.UserMaster.user_type.label("type"),
                                             ledger_master.LedgerMaster.Lgr_Id.label("id"),
                                             ledger_master.LedgerMaster.Lgr_Email.label("email"),
                                             ledger_master.LedgerMaster.Lgr_Add1,
                                             ledger_master.LedgerMaster.Lgr_Add2,
                                             ledger_master.LedgerMaster.Lgr_Add3,
                                             ledger_master.LedgerMaster.City_PinCode,
                                             CityMaster.city_name,
                                             StateMaster.state_name,
                                             ledger_master.LedgerMaster.GSTINNO.label("GSTINNO"),
                                             ) \
                    .join(ledger_master.LedgerMaster,
                          user_master.UserMaster.lgr_id == ledger_master.LedgerMaster.Lgr_Id) \
                    .join(StateMaster, ledger_master.LedgerMaster.State_Id == StateMaster.state_id) \
                    .join(CityMaster, ledger_master.LedgerMaster.City_Id == CityMaster.city_id) \
                    .filter(func.trim(func.lower(user_master.UserMaster.user_email)) == (user_id.strip().lower())) \
                    .all()
            else:
                return 'Invalid Email Address'

        if user_data is not None and len(user_data) > 0:
            json_list = [i._asdict() for i in user_data]
            # print(json_list)
            # print([j for j in json_list if j['email'] and j['email'].lower().strip() == user_id.lower()])
            # print(user_data._asdict())
            return jsonify(json_list)
        else:
            return "User Not Found"

    def checkIfUserExists(self, user_id):
        res = self.getuser(user_id)
        if type(res) == str:
            return 'False'
        else:
            return 'True'

    def getUserDetails(self):
        if request.method == 'POST':
            request_data = request.get_json()
            if 'user_id' in request_data:
                return self.getuser(request_data['user_id'])
        else:
            return "Method mot allowed!"

    def update(self, userId):
        pass

    def delete(self, userId):
        pass
