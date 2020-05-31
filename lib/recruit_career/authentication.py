import json

from lib.recruit_career.base import BaseClient


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