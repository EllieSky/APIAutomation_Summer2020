import random
import time
import unittest
import bs4
import requests
from faker import Faker
from lib2.hrm_authenticate import Authenticate


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_create_employee(self):
        sess = Authenticate()

        # Step 1: get the landing page - contains login form
        login_page = sess.login_page()

        # Step 2: extract CSRF token
        soup = bs4.BeautifulSoup(login_page.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'}) #input tag, attribute name
        token = result['value']

        # Step 3: login, by posting credentials + CSRF token
        authenticate_uri = '/auth/validateCredentials'

        login_data = {'_csrf_token': token,
                        'txtUsername': 'admin',
                        'txtPassword': 'password'
                        }
        resp = sess.login(login_data)

        self.assertIn('/pim/viewEmployeeList', resp.url)
        # OR
        self.assertTrue(resp.url.endswith('/pim/viewEmployeeList'))

        # Step 4:  get the add employee page  - contains the FORM to add employee
        #add_emp_uri = '/pim/addEmployee'
        #resp = self.sess.get(self.url + add_emp_uri)

        resp = sess.get_add_emp_page()

        # Step 5: Extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})  # input tag, attribute name
        token = result['value']

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
       # resp = self.sess.post(self.url + add_emp_uri, data=emp_data)

        resp = sess.add_employee(emp_data)

        self.assertIn('/pim/viewPersonalDetails/empNumber', resp.url)

        # Optional step, to check that data posted correctly
        #resp = self.sess.get(resp.url)

        resp = sess.confirm_data(resp.url)

        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']
        self.assertEqual(str(emp_id), actual_emp_id)

if __name__ == '__main__':
    unittest.main()
