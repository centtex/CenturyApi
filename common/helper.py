import re

from sqlalchemy import func
from models import db, user_master, ledger_master
from models.address_master import StateMaster, CityMaster


class Helper:
    def __init__(self):
        pass

    def get_user(self, user_id):
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
                    .filter(func.trim(func.lower(user_master.UserMaster.user_email)) == (user_id.strip().lower()),
                            user_master.UserMaster.isActive == 1) \
                    .all()
            else:
                return 'Invalid Email Address'

        if user_data is not None and len(user_data) > 0:
            json_list = [i._asdict() for i in user_data]
            return json_list
        else:
            return []

    def check_if_user_id_exist(self, user_id, request_user_id):
        if user_id is not None and request_user_id:
            user_details = self.get_user(user_id)
            user_ids = [user['id'] for user in user_details]
            check = all(item in user_ids for item in request_user_id)
            return check
        else:
            return False
