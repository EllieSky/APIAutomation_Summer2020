import json
import unittest

import requests
from parameterized import parameterized


class CareerPortalHomework2TestCase(unittest.TestCase):
    data = [
        ('correct application_id', 15, 200, 'OK', ''),
        ('incorrect application_id', 17, 400, 'Bad Request', 'Incorrect applicationId: 17'),
        ('letters', 'abc', 500, 'Internal Server Error', 'ER_BAD_FIELD_ERROR'),
        ('special characters', '@!', 500, 'Internal Server Error', 'ER_BAD_FIELD_ERROR'),
        ('space', ' ', 400, 'Bad Request', '')
    ]

    def setUp(self) -> None:
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 ('
                                      'KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

        # /login
        result = self.login()
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']
        authorization_header = {'Authorization': 'Bearer ' + token}
        authorization_header.update(self.headers)

        # /verify
        verify_response = self.verify(authorization_header)
        verify_content = json.loads(verify_response.content)

        self.user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, self.user_id)

    def test_positions(self):
        # /positions
        positions = self.get_positions()
        json_positions = json.loads(positions.text)
        self.assertGreater(len(json_positions), 3)

        # /candidates/{id}/positions
        candidate_positions = self.get_candidate_positions(self.user_id)
        json_candidate_positions = json.loads(candidate_positions.text)
        self.assertEqual(len(json_candidate_positions), 1)

    @parameterized.expand(data)
    def test_applications(self, test_name, application_id, status_code, reason, expected_error_message):
        # /applications
        applications = self.get_applications()
        json_applications = json.loads(applications.text)
        self.assertEqual(len(json_applications), 9)

        # /applications/{id}
        single_application = self.get_single_application(application_id)
        self.assertEqual(status_code, single_application.status_code)
        self.assertEqual(reason, single_application.reason)

        if single_application.status_code == 200:
            json_single_application = json.loads(single_application.text)
            self.assertEqual('Sample', json_single_application['firstName'])
            self.assertEqual('Director, Product Development', json_single_application['title'])

        if expected_error_message:
            json_single_application = json.loads(single_application.text)
            if 'code' in json_single_application:
                self.assertEqual(expected_error_message, json_single_application['code'])
            elif 'errorMessage' in json_single_application:
                self.assertEqual(expected_error_message, json_single_application['errorMessage'])

    def login(self):
        return requests.post(self.base_url + '/login',
                             json={"email": "student@example.com", "password": "welcome"})

    def verify(self, authorization_header):
        return requests.post(self.base_url + '/verify', headers=authorization_header)

    def get_positions(self):
        return requests.get(self.base_url + '/positions')

    def get_candidate_positions(self, user_id):
        return requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions')

    def get_applications(self):
        return requests.get(self.base_url + '/applications')

    def get_single_application(self, application_id):
        return requests.get(self.base_url + '/applications/' + str(application_id))


if __name__ == '__main__':
    unittest.main()
