from lib.recruit_career.base import BaseClient


class Positions(BaseClient):
    def get_all_positions(self):
        return self.session.get(self.base_url + '/positions')