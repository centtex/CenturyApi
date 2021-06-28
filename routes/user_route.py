from flask import Blueprint

from controllers.user_controller import UserController

controller = UserController()

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/', methods=['GET'])(controller.index)
user_bp.route('/create', methods=['POST'])(controller.store)
user_bp.route('/<int:user_id>', methods=['GET'])(controller.show)
user_bp.route('/<int:user_id>/edit', methods=['POST'])(controller.update)
user_bp.route('/<int:user_id>', methods=['DELETE'])(controller.delete)
