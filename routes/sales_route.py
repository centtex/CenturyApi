from flask import Blueprint

from controllers.sales_order_controller import SalesOrder
from controllers.sales_invoice_controller import SalesInvoiceController

order_controller = SalesOrder()
invoice_controller = SalesInvoiceController()

sales_bp = Blueprint('sales_bp', __name__)
sales_bp.route('/getSalesOrderDetails/<user_id>', methods=['POST'])(order_controller.getSalesOrderDetails)
sales_bp.route('/getInvoiceDetails/<user_id>', methods=['POST'])(invoice_controller.getInvoiceDetails)
