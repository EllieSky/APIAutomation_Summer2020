import json
import unittest

import requests
from parameterized import parameterized


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
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        self.authorization_header = {'Authorization': 'Bearer ' + token}
        self.authorization_header.update(self.headers)

    @parameterized.expand(applications_id_input_pos)
    def test_get_applications_id_pos(self, test_name, application_id, status_code, title):
        my_applications = requests.get(self.base_url + '/applications/' + str(application_id))
        self.assertEqual(status_code, my_applications.status_code)
        json_my_applications = json.loads(my_applications.text)
        self.assertEqual(json_my_applications['title'], title)

    @parameterized.expand(applications_id_input_neg)
    def test_get_applications_id_neg(self, test_name, application_id, status_code, error_message):
        my_applications = requests.get(self.base_url + '/applications/' + str(application_id))
        self.assertEqual(status_code, my_applications.status_code)
        json_my_applications = json.loads(my_applications.text)
        if my_applications.status_code == 500:
            self.assertEqual(json_my_applications['code'], error_message)
        else:
            self.assertEqual(json_my_applications['errorMessage'], error_message)

    @parameterized.expand(positions_input)
    def test_get_candidate_positions(self, test_name, user_id, status_code, error_message):
        my_positions = self.get_candidate_positions(user_id)
        self.assertEqual(status_code, my_positions.status_code)
        if my_positions.status_code != 204:
            json_my_positions = json.loads(my_positions.text)
            self.assertEqual(json_my_positions['code'], error_message)

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions',
                            headers=self.authorization_header)

    def login(self, email, password):
        return requests.post(self.base_url + '/login', json={"email": email, "password": password})


if __name__ == '__main__':
    unittest.main()
