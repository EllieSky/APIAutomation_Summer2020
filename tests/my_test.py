import json
import unittest
import requests

from lib.authentication import Authenticate


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
        sess = Authenticate()

        # get all positions
        positions = sess.get_all_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(5, len(json_positions))

        # authenticate/login/POST
        result = sess.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        # verify user/POST
        verify_response = sess.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        # verify user_ID
        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

        # get candidate position by user ID
        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)
        self.assertEqual(1, len(json_my_positions))

        # get all candidates
        candidates = sess.get_all_candidates()
        json_candidates = json.loads(candidates.text)
        self.assertEqual(60, len(json_candidates))

        # post new candidate
        new_candidate = sess.post_new_candidate('Nj', 'Candkjidate', 'nd@example.com', 'delete')
        json_new_candidate = json.loads(new_candidate.text)
        self.assertEqual('Candkjidate', json_new_candidate['lastName'])
        new_candidate_id = json_new_candidate['id']
        print(new_candidate_id)


        # delete candidate using ID
        delete_candidate = sess.delete_candidate_by_id(new_candidate_id)
        self.assertEqual()
        # i don't know how to finish it((

    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
