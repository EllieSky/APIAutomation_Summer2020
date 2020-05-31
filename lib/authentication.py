import json
from lib.base import BaseClient


class Authenticate(BaseClient):
    def authenticate(self, email, password):
        resp = self.session.post(self.base_url + '/login', json={"email": email, "password": password})
        json_parsed = json.loads(resp.text)
        token = json_parsed.get('token', None)
        if token:
            self.session.headers.update({'Authorization': 'Bearer ' + token})
        return resp

    def perform_user_verification(self):
        return self.session.post(self.base_url + '/verify')

    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')
