import json
import unittest

import data as data
import requests
from lib2.authentication import Authenticate

class YahooAPITestCase(unittest.TestCase):
    def test_for_successful_response(self):
        result = requests.get("http://www.yahoo.com")
        self.assertEqual(200, result.status_code)
        # OR
        self.assertTrue('OK' == result.reason)

class CareerPortalTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_login(self):
        sess = Authenticate() #sess is an object of class, creates instance of class
        positions = sess.get_all_positions()
        json_positions = json.loads(positions.text)
        self.assertEqual(5, len(json_positions))

        application = sess.get_application(1)
        json_application = json.loads(application.text)
        self.assertEqual(1, json_application['id'])

        result = sess.authenticate('student@example.com', 'welcome')
        self.assertEqual(200, result.status_code)

        verify_response = sess.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue('student@example.com', email)
        self.assertEqual(8, user_id)

        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(1, len(json_my_positions))

    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])

    def test_get_all_candidates(self):
        sess = Authenticate()
        all_candidates = sess.get_all_candidates()
        json_all_candidates = json.loads(all_candidates.text)
        count1 = len(json_all_candidates)
        print('Total number of candidates: ' + str(count1))

    def test_add_candidate(self):
        sess = Authenticate()
        all_candidates = sess.get_all_candidates()
        json_all_candidates = json.loads(all_candidates.text)
        count1 = len(json_all_candidates)
        print('Total number of candidates first: ' + str(count1))
       # candidate_details = {'firstName': 'Soniya', 'lastName': 'Singhal', 'email': 'ssinghal22@yahoo.com', 'password': 'abc123.', 'id': 20, 'positionsCount': 0}

        firstName = 'Soniya'
        lastName = 'Singhal'
        email = 'ssinghal13@yahoo.com'
        password = 'abc123.'
        add_candidate = sess.add_candidate(firstName, lastName, email, password)
        json_add_candidate = json.loads(add_candidate.text)
        id = json_add_candidate['id']
        print('id of added candidate is: ' + str(id))

        all_candidates = sess.get_all_candidates()
        json_all_candidates = json.loads(all_candidates.text)
        count2 = len(json_all_candidates)
        print('Total number of candidates now: ' + str(count2))
        self.assertGreater(count2, count1)

        ids = []
        for elem in json_all_candidates:
            ids.append(elem['id'])

        if id in ids:
            print('Candidate found with id: ' + str(id))

        # sess.authenticate('student@example.com', 'welcome') #login type 1
        sess.authenticate(email, password)  #login type 2

        delete_candidate = sess.delete_added_candidate(id)
        self.assertEqual(204, delete_candidate.status_code)

        all_candidates = sess.get_all_candidates()
        json_all_candidates = json.loads(all_candidates.text)

        ids = []
        for elem in json_all_candidates:
            ids.append(elem['id'])

        if id not in ids:
            print('Candidate not found with id: ' + str(id))


if __name__ == '__main__':
    unittest.main()
