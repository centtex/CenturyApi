from flask import Blueprint

from controllers.address_controller import AddressController

controller = AddressController()

add_bp = Blueprint('add_bp', __name__)
add_bp.route('/', methods=['GET'])(controller.index)
