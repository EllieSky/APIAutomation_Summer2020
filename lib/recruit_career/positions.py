import requests

from lib.recruit_career.base import BaseClient


class Positions(BaseClient):
    def get_all_positions(self):
        return self.session.get(self.base_url + '/positions')


def get_candidate_positions (base_url, authorization_header, user_id):
    return requests.get(base_url + '/candidates/' + str(user_id) + '/positions', headers =authorization_header)