import os
import time
import random
import unittest
import bs4

from requests import Session
from faker import Faker
from requests_toolbelt import MultipartEncoder

from lib.hrm.steps import HRM, PersonalDetails


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.hrm = HRM()
        self.f = Faker()

    def tearDown(self) -> None:
        self.hrm.close()

    def test_create_employee(self):
        resp = self.hrm.login()

        self.assertIn('/pim/viewEmployeeList', resp.url)
        # OR
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        emp_number = str(time.time()).split('.')[-1]
            # OR
        emp_number = random.randrange(100000, 999999)
            # OR
        f = self.f

        first_name = f.first_name()
        last_name = f.last_name()
        emp_number = str(f.random_number(6))

        file_path = os.path.abspath("../download.jpeg")

        resp = self.hrm.add_employee(emp_number, first_name, last_name, file_path)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # Optional step, to check that data posted correctly
        resp = self.hrm.get_employee_details(resp.url)
        # soup = bs4.BeautifulSoup(resp.content, 'html5lib')

        actual_emp_id = resp.html_data.select_one('#personal_txtEmployeeId')['value']

        self.assertEqual(str(emp_number), actual_emp_id)

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

    def test_edit_personal_details(self):
        emp_number = 3450

        self.hrm.login()

        nick_name = self.f.word().title()
        ssn = self.f.ssn()

        resp = self.hrm.update_employee_personal_details(emp_number,
                                                         (PersonalDetails.NICK_NAME, nick_name),
                                                         (PersonalDetails.SSN, ssn))
        # soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        txtEmpNickName = resp.html_data.find(attrs={'name': 'personal[txtEmpNickName]'})['value']

        self.assertEqual(nick_name, txtEmpNickName)

if __name__ == '__main__':
    unittest.main()
