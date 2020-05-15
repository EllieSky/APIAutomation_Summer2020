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

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        self.authorization_header = {'Authorization': 'Bearer ' + token}
        self.authorization_header.update(self.headers)

    @parameterized.expand(data)
    def test_get_candidate_positions(self, test_name, user_id, status_code, reason, expected_error_message):

        my_positions = self.get_candidate_positions(user_id)
        self.assertEqual(status_code, my_positions.status_code)
        self.assertEqual(reason, my_positions.reason)

        if expected_error_message:
            json_my_positions = json.loads(my_positions.text)
            self.assertEqual(json_my_positions['code'], expected_error_message)

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions', headers = self.authorization_header)

if __name__ == '__main__':
    unittest.main()
