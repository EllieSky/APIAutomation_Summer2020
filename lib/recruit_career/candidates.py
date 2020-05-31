from lib.recruit_career.base import BaseClient


class Candidates(BaseClient):

    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')