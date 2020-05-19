import json

import requests


class Authenticate(object):
    def __init__ (self):
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        )

    def get_all_positions(self):
        return requests.get(self.base_url + '/positions')

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
