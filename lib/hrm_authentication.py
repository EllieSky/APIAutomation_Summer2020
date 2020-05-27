import json
import requests
from bs4 import BeautifulSoup
from faker import Faker


class HRMAuthentication(object):
    def __init__(self):
        self.base_url = 'http://hrm-online.portnov.com/symfony/web/index.php'
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})

    def authenticate(self, uname, password):
        login_uri = "/auth/login"
        resp = self.session.get(self.base_url + login_uri)

        soup = BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})
        token = result['value']
        authenticate_uri = '/auth/validateCredentials'

        login_data = {
            '_csrf_token': token,
            'txtUsername': uname,
            'txtPassword': password
        }
        return self.session.post(self.base_url + authenticate_uri, data=login_data)

    def get_add_employee_page(self, add_emp_uri):
        return self.session.get(self.base_url + add_emp_uri)

    def get_CSRF_token(self, resp):
        soup = BeautifulSoup(resp.content, 'html5lib')
        return soup.find('input', attrs={'name': '_csrf_token'})['value']

    def get_random_created_employee_with_csrf_token(self, token):
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
        return emp_data

    def add_employee(self, emp_data):
        add_emp_uri = "/pim/addEmployee"
        return self.session.post(self.base_url + add_emp_uri, data=emp_data)

    def get(self, url):
        return self.session.get(url)

    def submit_candidate_application(self, submit_data):
        submit_candidate_app = "/recruitment/addCandidate"
        self.session.post(self.base_url + submit_candidate_app, data=submit_data)





