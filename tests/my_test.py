import json
import unittest
import requests

from lib.recruit_career.authentication import Authenticate
from lib.recruit_career.rc_client import RecruitClient


class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response (self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)


class CareerPortalTests(unittest.TestCase):
    def setUp (self) -> None:
        pass

    def test_login (self):
        client = RecruitClient()
        # client.authentication.authenticate('jane@example.com', 'pass')

        # # if you want parallel clients
        # client2 = RecruitClient()
        # client2.authentication.authenticate('bob@example.com', 'Boo')
        #
        # # using A to instantiate P
        #
        # auth_client = Authenticate()
        # auth_client.authenticate()
        #
        # pos_client = Positions(auth_client)

<<<<<<< HEAD
        #############

        positions = client.positions.get_all_positions()
        json_positions = json.loads(positions.text)
=======
        # get all positions
        positions = sess.get_all_positions()
        # parse response to json format
        json_positions = json.loads(positions.text)
        self.assertEqual(6, len(json_positions))
>>>>>>> homework3, test add_candidate_app - need to be modified

        self.assertIsInstance(json_positions, list)
        self.assertGreaterEqual(len(json_positions), 5)

        result = client.authentication.authenticate("student@example.com", "welcome")

        sess = Authenticate()
        # authenticate/login/POST
        result = sess.authenticate("student@example.com", "welcome")

        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        verify_response = client.authentication.perform_user_verification()

        verify_content = json.loads(verify_response.content)

        # verify user_ID
        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

<<<<<<< HEAD
    def test_cannot_login (self):
=======
        # get candidate position by user ID
        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)
        self.assertEqual(3, len(json_my_positions))

        # get all candidates
        candidates = sess.get_all_candidates()
        json_candidates = json.loads(candidates.text)
        self.assertEqual(38, len(json_candidates))

        # post new candidate
        new_candidate = sess.post_new_candidate('Nj', 'Candkjidate', 'nd@example.com', 'delete')
        json_new_candidate = json.loads(new_candidate.text)
        self.assertEqual('Candkjidate', json_new_candidate['lastName'])
        new_candidate_id = json_new_candidate['id']
        print(new_candidate_id)


    def test_cannot_login(self):
>>>>>>> homework3, test add_candidate_app - need to be modified
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
