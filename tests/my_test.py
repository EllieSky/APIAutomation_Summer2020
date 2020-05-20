import json
import unittest
import requests

class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response(self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)

class CareerPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    def get_all_positions(self):
        return requests.get(self.base_url + '/positions')

    def authenticate(self, aemail, apassword):
        return requests.post(self.base_url + '/login', json={"email": aemail, "password": apassword})

    def perform_user_verification(self, token):
        verify_header = {'Authorization': 'Bearer ' + token}
        verify_header.update(self.headers)
        return requests.post(self.base_url + '/verify', headers=verify_header)

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

    def get_application(self, id):
        return requests.get(self.base_url + '/applications/' + str(id))

    def test_login(self):
        positions = self.get_all_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(5, len(json_positions))

        application = self.get_application(1)
        json_application = json.loads(application.text)
        self.assertEqual(aid, json_application['id'])

        result = self.authenticate('student@example.com', 'welcome')
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        verify_response = self.perform_user_verification(token)
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == aemail)
        self.assertEqual(8, user_id)

        my_positions = self.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(len(json_my_positions), 3)


if __name__ == '__main__':
    unittest.main()
