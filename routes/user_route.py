from flask import Blueprint

from controllers.user_controller import UserController

controller = UserController()

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/', methods=['GET'])(controller.index)
user_bp.route('/checkIfUserExists/<user_id>', methods=['POST'])(controller.checkIfUserExists)
user_bp.route('/getUserDetails/', methods=['POST'])(controller.getUserDetails)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(controller.update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(controller.delete)
