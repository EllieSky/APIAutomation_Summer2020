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
        positions = requests.get(self.base_url + '/positions')
        json_positions = json.loads(positions.text)

        self.assertEqual(len(json_positions), 5)

        result = requests.post(self.base_url + '/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        token = json_parsed['token']

        verify_header = {'Authorization': 'Bearer ' + token}
        verify_header.update(self.headers)

        verify_response = requests.post(self.base_url + '/verify', headers=verify_header)
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

        my_positions = requests.get(self.base_url + '/candidates/' + str(user_id) + '/positions')
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(len(json_my_positions), 2)


if __name__ == '__main__':
    unittest.main()
