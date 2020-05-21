import json
import unittest
import requests

from lib.authentication import Authenticate


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
        sess = Authenticate()
        positions = sess.get_all_positions()
        json_positions = json.loads(positions.text)

        self.assertEqual(5, len(json_positions))

        result = sess.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])

        verify_response = sess.perform_user_verification()
        verify_content = json.loads(verify_response.content)

        user_id = verify_content['id']
        email = verify_content['email']

        self.assertTrue(email == 'student@example.com')
        self.assertEqual(8, user_id)

        my_positions = sess.get_candidate_positions(user_id)
        json_my_positions = json.loads(my_positions.text)

        self.assertEqual(1, len(json_my_positions))

    def test_cannot_login(self):
        sess = Authenticate()
        response = sess.authenticate('foo', 'barr')
        json_parsed = json.loads(response.text)
        self.assertEqual('Incorrect email: foo', json_parsed['errorMessage'])

    def test_get_candidates_number(self):
        sess = Authenticate()
        sess.authenticate("student@example.com", "welcome")
        candidates = sess.get_candidates()
        number_of_candidate = json.loads(candidates.text).__len__()
        print("The number of candidates is: " + str(number_of_candidate))

    def test_create_and_delete_candidate(self):
        sess = Authenticate()
        sess.authenticate("student@example.com", "welcome")
        self.email = 'peter@pan.com'
        self.password = 'test'
        response_data = sess.create_candidate('peter', 'pan', self.email, self.password)
        self.id = json.loads(response_data.text)['id']
        print(self.id)
        candidate_status = requests.get('https://recruit-portnov.herokuapp.com/recruit/api/v1/candidates/' + str(self.id))
        self.assertEqual(200, candidate_status.status_code)
        print("candidate got created!")
        response = sess.delete_candidate(self.id)
        candidate_status = requests.get('https://recruit-portnov.herokuapp.com/recruit/api/v1/candidates/' + str(self.id))
        self.assertEqual(400, candidate_status.status_code)
        print("verify candidate is deleted(not there)!")

    def test_create_and_login(self):
        sess = Authenticate()
        self.email = 'peter@pan.com'
        self.password = 'test'
        response_data = sess.create_candidate('peter', 'pan', self.email, self.password)
        self.id = json.loads(response_data.text)['id']
        sess.authenticate(self.email, self.password)
        candidates = sess.get_candidates()
        number_of_candidate = json.loads(candidates.text).__len__()
        print("The number of candidates is: " + str(number_of_candidate))
        candidate_list = json.loads(candidates.text)
        id_array = []
        for i in range(0, number_of_candidate):
            id_array.append(candidate_list[i]['id'])
        self.assertTrue(self.id in id_array)
        sess.delete_candidate(self.id)
        id_array.remove(self.id)
        id_array = []
        candidates = sess.get_candidates()
        number_of_candidate = json.loads(candidates.text).__len__()
        for i in range(0, number_of_candidate):
            id_array.append(candidate_list[i]['id'])
        self.assertFalse(self.id in id_array)


    def test_delete_candidate(self):
        sess = Authenticate()
        sess.authenticate("student@example.com", "welcome")
        candidates = sess.get_candidates()
        candidate_list = json.loads(candidates.text)
        number_of_candidate = json.loads(candidates.text).__len__()
        id_array = []
        for i in range(0, number_of_candidate):
            if candidate_list[i]['firstName'] == 'peter':
                id_array.append(candidate_list[i]['id'])
                response = sess.delete_candidate(candidate_list[i]['id'])
        print(response)

    def test_new_candidate_login(self):
        sess = Authenticate()
        self.email = 'test@example.com'
        self.password = 'test'
        response = sess.authenticate("student@example.com", "welcome")
        print(response)



if __name__ == '__main__':
    unittest.main()
