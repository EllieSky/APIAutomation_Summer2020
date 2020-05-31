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


        # verify user/POST
        verify_response = client.authentication.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        # # verify user_ID
        # user_id = verify_content['id']
        # email = verify_content['email']






    def test_cannot_login (self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])


if __name__ == '__main__':
    unittest.main()
