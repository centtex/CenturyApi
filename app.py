from flask import Flask
from flask_migrate import Migrate
from models import db

from config import config_names
from routes.user_route import user_bp
from routes.address_route import add_bp
from routes.company_route import cmp_bp
from routes.sales_route import sales_bp
from routes.packingslip_route import packingslip_bp
from routes.admin_route import admin_bp
from routes.outstanding_route import outstanding_bp

app = Flask(__name__)
app.config.from_object(config_names['default'])
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(add_bp, url_prefix='/address')
app.register_blueprint(cmp_bp, url_prefix='/company')
app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(packingslip_bp, url_prefix='/packingslip')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(outstanding_bp, url_prefix='/outstanding')


@app.route('/')
def index():
    return "Hello"


if __name__ == '__main__':
    app.run()
