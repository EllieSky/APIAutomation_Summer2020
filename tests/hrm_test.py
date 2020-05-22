import os
import unittest
import bs4
from requests import Session
from faker import Faker
from requests_toolbelt import MultipartEncoder
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


class HRMTestCase(unittest.TestCase):
    def setUpClass(self) -> None:
        self.url = 'http://hrm-online.portnov.com/symfony/web/index.php/auth'

        self.sess = Session()
        self.sess.headers.update({'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})











if __name__ == '__main__':
    unittest.main()
