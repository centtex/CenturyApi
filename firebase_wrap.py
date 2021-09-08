import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
from functools import wraps
import re
from flask import request


class FirebaseAuthenticate:
    cred = credentials.Certificate("century-group-29298.json")
    firebase_admin.initialize_app(cred)

    @staticmethod
    def get_user_token(user_id):
        db = firestore.client()
        users_ref = db.collection(u'users')
        docs = users_ref.stream()
        user_list = []
        for doc in docs:
            user_list.append(doc.to_dict())
            # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        try:
            user_id = int(user_id)
        except:
            pass

        if user_id and type(user_id) is int:
            if len(str(user_id)) == 10 and user_id != 9999999999:
                # res = [user for user in user_list if user['mobile'].strip() == str(user_id).strip()]
                if [user for user in user_list if user['mobile'].strip() == str(user_id).strip()]:
                    return True
                else:
                    return False

            else:
                return False
        else:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if re.match(regex, user_id):
                if [user for user in user_list if user['email'].strip().lower() == user_id.strip().lower()]:
                    return True
                else:
                    return False

            else:
                return False

    def check_token(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if not request.headers.get('user_id'):
                return {'message': 'No user id provided'}, 400
            try:
                user_id = request.headers.get('user_id')
                u_list = self.get_user_token()
                if [user for user in u_list if user['Mobile'] == user_id]:

                    return 1
                else:
                    return 0

                # user = auth.verify_id_token(request.headers['authorization'])
                # request.user = user
            except:
                return {'message': 'User is not authenticated.'}, 400
            # return f(*args, **kwargs)
            return f(*args, **kwargs)

        return wrap
