from flask import Blueprint

from controllers.company_controller import CompanyController

controller = CompanyController()

cmp_bp = Blueprint('cmp_bp', __name__)
cmp_bp.route('/', methods=['GET'])(controller.index)
cmp_bp.route('/getCompanyDetails/<company_id>', methods=['POST'])(controller.getCompanyDetails)
