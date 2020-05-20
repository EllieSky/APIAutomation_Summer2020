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
        sess = Authenticate() #sess is an object of class, creates instance of class
        positions = sess.get_all_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(5, len(json_positions))

        application = sess.get_application(1)
        json_application = json.loads(application.text)
        self.assertEqual(1, json_application['id'])

        result = sess.authenticate('student@example.com', 'welcome')
        self.assertEqual(200, result.status_code)

        verify_response = sess.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue('student@example.com', email)
        self.assertEqual(8, user_id)

        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(1, len(json_my_positions))


if __name__ == '__main__':
    unittest.main()
