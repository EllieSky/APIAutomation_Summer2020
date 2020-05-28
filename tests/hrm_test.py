import unittest

from lib.hrm_online import HrmOnline


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sess = HrmOnline()

    def test_create_employee(self):
        resp = self.sess.login('admin', 'password')
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        emp_data = self.sess.generate_emp_json()
        resp = self.sess.add_emp(emp_data)
        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        actual_emp_id = self.sess.extract_emp_id(resp)
        self.assertEqual(str(emp_data['employeeId']), actual_emp_id)


if __name__ == '__main__':
    unittest.main()