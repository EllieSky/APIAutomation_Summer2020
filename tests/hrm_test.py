import os
import random
import time
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
        emp_number = f.random_number(6)

        file_path = os.path.abspath("../download.jpeg")

        resp = self.hrm.add_employee(emp_number, first_name, last_name, img_file=file_path)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # Optional step, to check that data posted correctly
        resp = self.hrm.get_employee_details(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')

        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']

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


if __name__ == '__main__':
    unittest.main()
