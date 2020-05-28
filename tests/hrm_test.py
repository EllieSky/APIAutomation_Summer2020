import unittest

from lib.hrm_online import HrmOnline


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sess = HrmOnline()

    def test_create_employee(self):
        resp = self.sess.login('admin', 'password')
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        emp_data = self.sess.generate_emp_data()
        resp = self.sess.add_emp(emp_data)
        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        actual_emp_id = self.sess.extract_emp_id(resp)
        self.assertEqual(str(emp_data['employeeId']), actual_emp_id)

    def test_create_candidate(self):
        resp = self.sess.login('admin', 'password')
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        cand_data = self.sess.generate_cand_data()
        resp = self.sess.add_candidate(cand_data)
        self.assertIn('/recruitment/addCandidate/id/', resp.url)

        actual_cand_data = self.sess.extract_cand_data(resp)
        self.assertEqual(cand_data, actual_cand_data)


if __name__ == '__main__':
    unittest.main()
