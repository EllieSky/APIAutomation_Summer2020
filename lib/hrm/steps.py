import os
import re

import bs4
import requests
from requests_toolbelt import MultipartEncoder


class HRM():
    def __init__(self):
        self.url = "http://hrm-online.portnov.com/symfony/web/index.php"
        self.sess = requests.Session()
        self.sess.headers.update(
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 " +
                           "(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"})

    def login(self, username='admin', password='password'):
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
            'txtUsername': username,
            'txtPassword': password
        }

        return self.sess.post(self.url + authenticate_uri, data=login_data)

    def add_employee(self, emp_id, first_name, last_name, middle_name='', img_file=None):
        # Step 1:  get the add employee page  - contains the FORM to add employee
        add_emp_uri = "/pim/addEmployee"
        resp = self.sess.get(self.url + add_emp_uri)

        # Step 2: Extract CSRF token
        # you need to install the html5lib package
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': '_csrf_token'})['value']

        file_name = os.path.basename(img_file)

        emp_data = {
            'firstName': first_name,
            'middleName': middle_name,
            'lastName': last_name,
            'employeeId': str(emp_id),
            'empNumber': str(emp_id),
            'photofile': (file_name, open(img_file, 'rb'), 'image/jpeg'),
            '_csrf_token': token
        }

        multipart_data = MultipartEncoder(fields=emp_data)

        # Step 3: add the employee  - posting the new employee data  + CSRF token
        self.sess.headers.update({'Content-Type': multipart_data.content_type})
        return self.sess.post(self.url + add_emp_uri, data=multipart_data.to_string())

    def get_employee_details(self, emp_id):
        """ Takes emp_id as a number, string, or as full / partial url """
        num_id = str(emp_id) if str(emp_id).isdigit() else None
        if not num_id:
            match = re.match(r'.*/(\d+)', emp_id)
            num_id = match.group(1) if match else None
        return self.sess.get(self.url + '/pim/viewPersonalDetails/empNumber/' + num_id)

    def close(self):
        self.sess.close()

    def add_candidate(self, first_name, last_name, email, resume):
        # Step 1:  get the add employee page  - contains the FORM to add employee
        add_candidate_uri = "/recruitment/addCandidate/id/"
        resp = self.sess.get(self.url + add_candidate_uri)

        # Step 2: Extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'id': 'addCandidate__csrf_token'})['value']

        file_name = os.path.basename(resume)

        multipart_data = MultipartEncoder(
            fields={
                'addCandidate[_csrf_token]': token,
                'addCandidate[firstName]': first_name,
                'addCandidate[lastName]': last_name,
                'addCandidate[resume]': (file_name, open(resume, 'rb'), 'text/plain'),
                'addCandidate[appliedDate]': '05-27-2020',
                'addCandidate[email]': email
            }
        )

        self.sess.headers.update({'Content-Type': multipart_data.content_type})

        # Step 3: add the candidate  - posting the candidate data  + CSRF token
        return self.sess.post(self.url + add_candidate_uri, data=multipart_data.to_string())
