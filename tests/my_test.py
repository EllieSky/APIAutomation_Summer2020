import json
import unittest
import requests

from lib.authentication import Authenticate
from lib.base import RecruitClient
from lib.positions import Positions


class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response(self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)


class CareerPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_login(self):
        client = RecruitClient()
        client.authentication.authenticate('jane@example.com', 'pass')

        client2 = RecruitClient()
        client2.authentication.authenticate('a@example.com', 'bb')

        # using A to instance P
        auth_client = Authenticate()
        auth_client.authenticate()

        pos_client = Positions(auth_client)

        positions = client.positions.get_all_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(6, len(json_positions))

        # authenticate/login/POST
        result = client.authentication.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        # verify user/POST
        verify_response = client.authentication.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        # verify user_ID
        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

        # get candidate position by user ID
        my_positions = client.candidate.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)
        self.assertEqual(3, len(json_my_positions))

        # get all candidates
        candidates = client.candidate.get_all_candidates()
        json_candidates = json.loads(candidates.text)
        self.assertEqual(38, len(json_candidates))

        # post new candidate
        new_candidate = client.candidate.post_new_candidate('Nj', 'Candkjidate', 'nd@example.com', 'delete')
        json_new_candidate = json.loads(new_candidate.text)
        self.assertEqual('Candkjidate', json_new_candidate['lastName'])
        new_candidate_id = json_new_candidate['id']
        print(new_candidate_id)


    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
