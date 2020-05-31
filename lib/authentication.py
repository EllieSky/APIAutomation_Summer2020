import json

from lib.base import BaseRequest


class Authenticate(BaseClient):
    def authenticate(self, email, password):
        json_data = {"email": email, "password": password}
        resp = self.session.post(self.base_url + '/login', json=json_data)
        json_parsed = json.loads(resp.text)
        token = json_parsed.get('token', None)
        if token:
            self.session.headers.update({'Authorization': 'Bearer ' + token})
        return resp

    def perform_user_verification(self):
        return self.session.post(self.base_url + '/verify')

# goal: token will be part of the session all the time we don't need to pass token to the func
# all functions need to be in 1 container, that session can be shared,all function can use it.
# We create new instance of this container it create new instance of the session and all
# funct-s can use it)
