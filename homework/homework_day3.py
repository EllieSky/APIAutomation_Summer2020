import json
import unittest

from lib.authentication import Authenticate


class CandidatesTestCase(unittest.TestCase):
    def test_candidates(self):
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
        new_candidate = sess.create_candidate('Svp', 'Train', 'svp.train@example.com', 'SvpTrain')
        self.assertEqual(201, new_candidate.status_code)
        self.assertEqual('Created', new_candidate.reason)
        self.assertEqual(sess.base_url + '/candidates', candidates.url)

        json_new_candidate = json.loads(new_candidate.text)
        self.assertEqual('Svp', json_new_candidate['firstName'])
        self.assertEqual('Train', json_new_candidate['lastName'])
        self.assertEqual('svp.train@example.com', json_new_candidate['email'])

        candidate_id = json_new_candidate['id']
        print(candidate_id)

        # POST /login as a new candidate to ensure the email/password combination work
        result = sess.authenticate("svp.train@example.com", "SvpTrain")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])
        self.assertTrue(json_parsed['token'])

        # GET /candidates to ensure the count of existing candidates increased
        candidates = sess.get_candidates()
        json_candidates = json.loads(candidates.text)
        self.assertGreater(len(json_candidates), number_of_candidates)

        # POST /login as a recruiter/hiring manager/admin user
        result = sess.authenticate("student@example.com", "welcome")
        self.assertEqual(200, result.status_code)

        json_parsed = json.loads(result.text)
        self.assertTrue(json_parsed['authenticated'])
        self.assertTrue(json_parsed['token'])

        # DELETE /candidates/{id} - Deletes a single candidate
        response = sess.delete_candidate(candidate_id)
        self.assertEqual(204, response.status_code)
        self.assertEqual('No Content', response.reason)


if __name__ == '__main__':
    unittest.main()
