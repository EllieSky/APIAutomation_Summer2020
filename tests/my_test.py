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
    def test_login(self):
        result = requests.post('https://recruit-portnov.herokuapp.com/recruit/api/v1/login', json={"email": "student@example.com", "password": "welcome"})
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])


if __name__ == '__main__':
    unittest.main()
