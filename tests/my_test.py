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

    def test_login(self):
        positions = self.get_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(len(json_positions), 5)

        aid = 1
        application = self.get_application(aid)
        json_application = json.loads(application.text)
        self.assertEqual(aid, json_application['id'])

        aemail = 'student@example.com'
        apassword = 'welcome'

        result = self.post_login(aemail, apassword)
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        verify_header = {'Authorization': 'Bearer ' + token}
        verify_header.update(self.headers)

        verify_response = self.post_verify(verify_header)
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == aemail)
        self.assertEqual(8, user_id)

        my_positions = self.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(len(json_my_positions), 3)

    def get_positions(self):
        return requests.get(self.base_url + '/positions')

    def post_login(self, aemail, apassword):
        return requests.post(self.base_url + '/login', json={"email": aemail, "password": apassword})

    def post_verify(self, verify_header):
        return requests.post(self.base_url + '/verify', headers=verify_header)

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

    def get_application(self, id):
        return requests.get(self.base_url + '/applications/' + str(id))

if __name__ == '__main__':
    unittest.main()
