import unittest
import bs4
from faker import Faker
from lib.HrmAuthentication import HrmAuthenticate

f = Faker()


class HRMTest(unittest.TestCase):
    def setUp (self) -> None:
        self.url = "http://hrm-online.portnov.com/symfony/web/index.php"
        self.sess = HrmAuthenticate()

    def test_create_employee (self):
        # Step 1: get the landing page - contains login form
        response = self.sess.login('admin', 'password')
        self.assertTrue(response.ok)
        self.assertIn('/pim/viewEmployeeList', response.url)
        # OR
        self.assertTrue(response.url.endswith('/pim/viewEmployeeList'))

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
