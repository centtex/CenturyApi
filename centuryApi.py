from flask import Flask
from flask_migrate import Migrate
from models import db

from config import config_names
from routes.user_route import user_bp
from routes.address_route import add_bp

app = Flask(__name__)
app.config.from_object(config_names['default'])
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(add_bp, url_prefix='/address')


@app.route('/')
def index():
    return "Hello"


if __name__ == '__main__':
    app.run()
