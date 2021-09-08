from flask import Blueprint

from controllers.packingslip_controller import PackingSlip

packingslip_controller = PackingSlip()

packingslip_bp = Blueprint('packingslip_bp', __name__)
packingslip_bp.route('/getpackingslipdetails/<user_id>', methods=['POST'])(packingslip_controller.getPackingSlip)
