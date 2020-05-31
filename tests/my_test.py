import json
import unittest
import requests

from lib.recruit_career.authentication import Authenticate
from lib.recruit_career.rc_client import RecruitClient


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
        # client.authentication.authenticate('jane@example.com', 'pass')

        # # if you wanter parallel clients
        # client2 = RecruitClient()
        # client2.authentication.authenticate('bob@example.com', 'Boo')
        #
        # # using A to instantiate P
        #
        # auth_client = Authenticate()
        # auth_client.authenticate()
        #
        # pos_client = Positions(auth_client)

        #############

        positions = client.positions.get_all_positions()
        json_positions = json.loads(positions.text)

        self.assertIsInstance(json_positions, list)
        self.assertGreaterEqual(len(json_positions), 5)

        result = client.authentication.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        verify_response = client.authentication.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

        my_positions = client.candidate.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertLessEqual(1, len(json_my_positions))

    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
