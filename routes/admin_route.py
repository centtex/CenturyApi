from flask import Blueprint

from controllers.admin_controller import AdminController

admin_controller = AdminController()

admin_bp = Blueprint('admin_bp', __name__)
admin_bp.route('/getAdminConfig/', methods=['POST'])(admin_controller.getConfiguration)
