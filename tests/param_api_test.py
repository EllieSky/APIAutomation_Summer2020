import json
import unittest

import requests
from parameterized import parameterized


<<<<<<< HEAD
class MyPositionsTests(unittest.TestCase):
    data = [
        ('candidate happy path', 1, 200, 'OK', ''),
        ('user does not exist', 9999, 204, 'No Content', ''),
        ('letters', 'abc', 500, 'Internal Server Error', 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 204, 'No Content', ''),
        ('empty', '', 404, 'Not Found', '')
    ]

    app_id_data = [
        ('app_id happy path', 1, 200, 'OK', ''),
        ('app id does not exist', 10, 204, 'No Content', ''),
        ('app id does not exist', 9000, 204, 'No Content', '')
    ]

    login_account_json = {"email": "student@example.com", "password": "welcome"}

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
=======
class MyPositionsTest(unittest.TestCase):
    positions_input = [
        ('user does not exist', 9999, 204, ''),
        ('letters', 'abc', 500, 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 204, '')
    ]
    applications_id_input_pos = [
        ('happy path', 2, 200, 'Principal Automation Engineer')
    ]
    applications_id_input_neg = [
        ('application does not exist', 222, 400, 'Incorrect applicationId: 222'),
        ('letters', 'abc', 500, 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 400, 'Incorrect applicationId: 0')
    ]

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

        result = self.login("student@example.com", "welcome")

    @parameterized.expand(applications_id_input_pos)
    def test_get_candidate_positions(self, test_name, user_id, exp_status_code, reason, expected_error_message):

        my_positions = self.get_candidate_positions(user_id)
        self.assertEqual(exp_status_code, my_positions.status_code)
        self.assertEqual(reason, my_positions.reason)

        if expected_error_message:
            json_my_positions = json.loads(my_positions.text)
            self.assertEqual(json_my_positions['code'], expected_error_message)

    @parameterized.expand(applications_id_input_pos)
    def test_get_applications_id(self, test_name, app_id, status_code, reason, expected_error_message):

        my_positions = self.get_candidate_positions(app_id)
        self.assertEqual(status_code, my_positions.status_code)
        self.assertEqual(reason, my_positions.reason)

        if expected_error_message:
            json_my_positions = json.loads(my_positions.text)
            self.assertEqual(json_my_positions['code'], expected_error_message)

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions', headers = self.authorization_header)

if __name__ == '__main__':
    unittest.main()
