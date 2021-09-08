from flask import Blueprint

from controllers.outstanding_controller import OutStandingController

outstanding_controller = OutStandingController()

outstanding_bp = Blueprint('outstanding_bp', __name__)
outstanding_bp.route('/getOutStandingDetails/<user_id>', methods=['POST'])(outstanding_controller.getOutStandingDetails)
