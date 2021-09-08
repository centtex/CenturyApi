from models import db
from models.company_master import CompanyMaster
from flask import jsonify


class CompanyController:

    def index(self):
        return 'hello'

    def getCompanyDetails(self, company_id):
        data = db.session.query(CompanyMaster.cmp_Code.label("Label"),
                                CompanyMaster.cmp_Name.label("CompanyName"),
                                CompanyMaster.cmp_Tin_No.label("TinNo"),
                                CompanyMaster.cmp_ServiceTax_No.label("ServiceTaxNo"),
                                CompanyMaster.cmp_Tds_No.label("TDSNo"),
                                CompanyMaster.cmp_Pan_No.label("PANNo"),
                                CompanyMaster.cmp_Alias.label("Alias"),
                                CompanyMaster.cmp_Inv_Hading.label("InvoiceHeading"),
                                CompanyMaster.cmp_Item_Hading.label("ItemHeading"),
                                CompanyMaster.cmp_Specification.label("Specification"),
                                CompanyMaster.cmp_Registration_No.label("RegistrationNo"),
                                CompanyMaster.cmp_Jurisdiction.label("Jurisdiction"),
                                CompanyMaster.cmp_Contact_Person.label("ContactPerson"),
                                CompanyMaster.cmp_Add1.label("Address1"),
                                CompanyMaster.cmp_Add2.label("Address2"),
                                CompanyMaster.cmp_City.label("City"),
                                CompanyMaster.cmp_Pincode.label("Pincode"),
                                CompanyMaster.cmp_State.label("State"),
                                CompanyMaster.cmp_Phone1.label("Phone1"),
                                CompanyMaster.cmp_Phone2.label("Phone2"),
                                CompanyMaster.cmp_Mobile.label("Mobile"),
                                CompanyMaster.cmp_Fax.label("Fax"),
                                CompanyMaster.cmp_Email.label("Email"),
                                CompanyMaster.cmp_Web.label("Website"),
                                CompanyMaster.GSTINNO.label("GSTNo"),
                                ) \
            .filter(CompanyMaster.cmp_Code == company_id).first()

        return jsonify(data._asdict())
