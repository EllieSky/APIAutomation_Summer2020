import json
import unittest
import requests
from parameterized import parameterized

class MyPositionsTests(unittest.TestCase):
    data = [
        ('user does not exist', 9999, 204, 'No Content', ''),
        ('letters', 'abc', 500, 'Internal Server Error', 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 204, 'No Content', ''),
        ('empty', '', 404, 'Not Found', '')
    ]

    data_application = [
        ('application does not exist', 9999, 400, 'Bad Request', ''),
        ('letters', 'abc', 500, 'Internal Server Error', 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 400, 'Bad Request', ''),
        ('empty', '', 200, 'OK', '')
    ]
    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        aemail = 'student@example.com'
        apassword = 'welcome'

        result = self.post_login(aemail, apassword)
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        self.authorization_header = {'Authorization': 'Bearer ' + token}
        self.authorization_header.update(self.headers)

    def post_login(self, aemail, apassword):
        return requests.post(self.base_url + '/login', json={"email": aemail, "password": apassword})

    @parameterized.expand(data)
    def test_get_candidate_positions(self, test_name, auser_id, astatus_code, areason, aexpected_error_message):
        my_positions = self.get_candidate_positions(auser_id)
        self.assertEqual(astatus_code, my_positions.status_code)
        self.assertEqual(areason, my_positions.reason)

        if aexpected_error_message:
            json_my_positions = json.loads(my_positions.text)
            self.assertEqual(aexpected_error_message, json_my_positions['code'])

    def get_candidate_positions(self, auser_id):
        return requests.get(self.base_url + '/candidates/' + str(auser_id) + '/positions', headers=self.authorization_header)


    @parameterized.expand(data_application)
    def test_get_application(self, test_name, application_id, astatus_code, areason, aexpected_error_message):
        application = self.get_application(application_id)
        self.assertEqual(astatus_code, application.status_code)
        self.assertEqual(areason, application.reason)

        if aexpected_error_message:
            json_application = json.loads(application.text)
            self.assertEqual(aexpected_error_message, json_application['code'])

    def get_application(self, application_id):
        return requests.get(self.base_url + '/applications/' + str(application_id))

if __name__ == '__main__':
    unittest.main()