import os
import unittest
import bs4
from faker import Faker
from lib.hrm.steps import HRM

class HRMTest(unittest.TestCase):

    def setUp(self) -> None:
        self.hrm = HRM()
        self.f = Faker()

    def tearDown(self) -> None:
        self.hrm.close()

    def test_create_employee (self):
        # Step 1: get the landing page - contains login form
        response = self.sess.login('admin', 'password')
        self.assertTrue(response.ok)
        self.assertIn('/pim/viewEmployeeList', response.url)

        f = self.f

        first_name = f.first_name()
        last_name = f.last_name()
        emp_number = f.random_number(6)

        file_path = os.path.abspath("../download.jpeg")

        resp = self.hrm.add_employee(emp_number, first_name, last_name, file_path)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # Optional step, to check that data posted correctly
        resp = self.hrm.get_employee_details(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')

        # actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']


    def test_submit_application(self):
        # Step 1: authenticate
        self.hrm.login()

        f = self.f

        first_name = f.first_name()
        last_name = f.last_name()
        email = f.email()

        resume = os.path.abspath("../git_usage.txt")

        resp = self.hrm.add_candidate(first_name, last_name, email, resume)

        self.assertIn('/recruitment/addCandidate/id/', resp.url)

        # Step 4:  get the add employee page  - contains the FORM to add employee
        emp_id = f.random_number(6)
        resp = self.sess.add_employee(emp_id)
        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # # Optional step, to check that data posted correctly with verification
        # same_employee = self.sess.verify_candidate_data(resp.url)
        # self.assertTrue(same_employee)


     # Optional step, to check that data posted correctly
        resp = self.sess.verify_candidate_data(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']
        self.assertEqual(str(emp_id), actual_emp_id)

if __name__ == '__main__':
    unittest.main()


