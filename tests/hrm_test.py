import time
import random
import unittest
from bs4 import BeautifulSoup
from lib.hrm_authentication import HRMAuthentication
from requests import Session
from faker import Faker

class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_add_employee(self):
        sess = HRMAuthentication()
        sess.authenticate("admin", "password")
        resp_emp = sess.get_add_employee_page("/pim/addEmployee")
        csrf_token = sess.get_CSRF_token(resp_emp)
        emp_data = sess.get_random_created_employee_with_csrf_token(csrf_token)
        resp_verify = sess.add_employee(emp_data)

if __name__ == '__main__':
    unittest.main()

