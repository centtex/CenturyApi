from flask import jsonify, request
from models import db
from sqlalchemy.sql import text


class AdminController:
    def __init__(self):
        pass

    def getConfiguration(self):
        if request.method == 'POST':
            request_data = request.get_json()
            sql_stmt = 'SELECT `KEY`, `VALUE` FROM Configuration;'
            config_data = db.session.execute(text(sql_stmt), {"db": "classicmodels"})
            config_data_list = [slip._asdict() for slip in config_data.all()]
            return jsonify(config_data_list)

    def getAllUsers(self):
        # get all registered users with active status
        # get newly registered users with active status
        #
        if request.method == 'POST':
            request_data = request.get_json()

    # post call for deleting/inactive user

