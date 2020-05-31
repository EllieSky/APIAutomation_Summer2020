import requests

from lib.base import BaseClient


class Candidates(BaseClient):
    def get_all_candidates(self):
        return self.session.get(self.base_url + '/candidates')


    def post_new_candidate (self, first_name, last_name, email, password):
        json_data = {"firstName": first_name, "lastName": last_name, "email": email, "password": password}
        return self.session.post(self.base_url + '/candidates', json=json_data)


    def delete_candidate_by_id (self, candidate_id):
        return self.session.delete(self.base_url + '/candidates/' + str(candidate_id))


    def get_candidate_positions(self, user_id):
        return self.session.get(self.base_url + '/candidates/' + str(user_id) + '/positions')