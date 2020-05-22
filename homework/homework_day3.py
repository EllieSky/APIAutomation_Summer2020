import json
import unittest

from faker import Faker

from config import USER_NAME, PASSWORD
from lib.authentication import Authenticate, find_candidate_by_id


class CandidatesTestCase(unittest.TestCase):
    def test_candidates(self):
        f = Faker()

        first_name = f.first_name()
        last_name = f.last_name()
        email = f.email()
        password = f.password(8)

        sess = Authenticate()

        # GET /candidates - Returns all candidates
        candidates = sess.get_candidates()
        self.assertEqual(200, candidates.status_code)
        self.assertEqual('OK', candidates.reason)
        self.assertEqual(sess.base_url + '/candidates', candidates.url)

        json_candidates = json.loads(candidates.text)
        number_of_candidates = len(json_candidates)

        # TODO Check if candidate with associated email already exists (otherwise 500 error)

        # POST /candidates - Creates a new candidate
        new_candidate = sess.create_candidate(first_name, last_name, email, password)
        self.assertEqual(201, new_candidate.status_code)
        self.assertEqual('Created', new_candidate.reason)
        self.assertEqual(sess.base_url + '/candidates', candidates.url)

        json_new_candidate = json.loads(new_candidate.text)
        self.assertEqual(first_name, json_new_candidate['firstName'])
        self.assertEqual(last_name, json_new_candidate['lastName'])
        self.assertEqual(email, json_new_candidate['email'])

        candidate_id = json_new_candidate['id']
        print(candidate_id, first_name, last_name, email, password)

        # POST /login as a new candidate to ensure the email/password combination work
        result = sess.authenticate(email, password)
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])
        self.assertTrue(json_parsed['token'])

        # GET /candidates to ensure the count of existing candidates increased
        candidates = sess.get_candidates()
        json_candidates = json.loads(candidates.text)
        self.assertGreater(len(json_candidates), number_of_candidates)

        # Ensure created candidate is found among all candidates
        candidate = find_candidate_by_id(json_candidates, candidate_id)
        self.assertTrue(candidate, 'Candidate not found')
        self.assertEqual(first_name, candidate['firstName'])
        self.assertEqual(last_name, candidate['lastName'])
        self.assertEqual(email, candidate['email'])

        # POST /login as a recruiter/hiring manager/admin user
        result = sess.authenticate(USER_NAME, PASSWORD)
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])
        self.assertTrue(json_parsed['token'])

        # DELETE /candidates/{id} - Deletes a single candidate
        response = sess.delete_candidate(candidate_id)
        self.assertEqual(204, response.status_code)
        self.assertEqual('No Content', response.reason)

        # GET /candidates
        candidates = sess.get_candidates()
        json_candidates = json.loads(candidates.text)

        # Ensure deleted candidate is not found among all candidates
        candidate = find_candidate_by_id(json_candidates, candidate_id)
        self.assertFalse(candidate)


if __name__ == '__main__':
    unittest.main()
