import time
import random
import unittest
import bs4
<<<<<<< HEAD
=======
from requests import Session
from  faker import Faker
>>>>>>> hrm

from requests import Session
from faker import Faker


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://hrm-online.portnov.com/symfony/web/index.php"

        self.sess = Session()
        self.sess.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"})



    def test_create_employee(self):


        # Step 1: get the landing page - contains login form
        login_uri = "/auth/login"
        resp = self.sess.get(self.url + login_uri)

        # Step 2: extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})
        token = result['value']

        authenticate_uri = '/auth/validateCredentials'

        # Step 3: login, by posting credentials + CSRF token
        login_data = {
            '_csrf_token': token,
            'txtUsername': 'admin',
            'txtPassword': 'password'
        }

        resp = self.sess.post(self.url + authenticate_uri, data=login_data)

        self.assertIn('/pim/viewEmployeeList', resp.url)
        # OR
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))


        # Step 4:  get the add employee page  - contains the FORM to add employee
        add_emp_uri = "/pim/addEmployee"
        resp = self.sess.get(self.url + add_emp_uri)

        # Step 5: Extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': '_csrf_token'})['value']

        emp_id = str(time.time()).split('.')[-1]
            # OR
        emp_id = random.randrange(100000, 999999)
            # OR
        f = Faker()

        first_name = f.first_name()
        last_name = f.last_name()
        emp_id = f.random_number(6)

        emp_data = {
            'firstName': first_name,
            'lastName': last_name,
            'employeeId': emp_id,
            '_csrf_token': token
        }

        # Step 6: add the employee  - posting the new employee data  + CSRF token

        resp = self.sess.post(self.url + add_emp_uri, data=emp_data)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # Optional step, to check that data posted correctly
        resp = self.sess.get(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')

        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']

        self.assertEqual(str(emp_id), actual_emp_id)

<<<<<<< HEAD
=======
class HRMTestCase(unittest.TestCase):
    def setUpClass(self) -> None:
        self.url = 'http://hrm-online.portnov.com/symfony/web/index.php/auth'

        self.sess = Session()
        self.sess.headers.update({'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})

    def test_create_employee(self):
        login_url = '/login'
        resp = self.sess.get(self.url + login_url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attr = {'name': '_csrf_token'})
        token = result['value']

        authenticate_url = 'validateCredentials'

        login_data = {
            '_csrf_token': token,
            'txtUsername': 'admin',
            'txtPassword': 'password'
        }

        resp = self.sess.post(self.url + authenticate_url, data= login_data)


        self.assertIn('viewEmployeeLis', resp.url)

        f = Faker
        first_name = f.first_name()
        last_name = f.last_name()
>>>>>>> hrm


if __name__ == '__main__':
    unittest.main()
