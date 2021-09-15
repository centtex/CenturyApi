from flask import jsonify, request
from common.helper import Helper


class UserController:

    def __init__(self):
        self.helper = Helper()

    def index(self):
        return "UserApi"

    def checkIfUserExists(self, user_id):
        res = self.helper.get_user(user_id)
        if type(res) == str:
            return 'False'
        else:
            return 'True'

    def getUserDetails(self):
        if request.method == 'POST':
            request_data = request.get_json()
            if 'user_id' in request_data:
                user_list = self.helper.get_user(request_data['user_id'])
                if user_list and len(user_list) > 0:
                    return jsonify(user_list)
                else:
                    return "User Not Found"
        else:
            return "Method mot allowed!"

    def update(self, userId):
        pass

    def delete(self, userId):
        pass
