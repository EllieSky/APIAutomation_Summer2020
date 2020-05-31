import requests

from lib.base import BaseRequest


class Positions(BaseRequest):
    def get_all_positions(self):
        return self.session.get(self.base_url + '/positions')
