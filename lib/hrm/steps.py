import os
import re

import bs4
import requests


class HRM:
    FIELD_NAMES = {
        '_csrf_token',
        'txtEmpID',
        'txtEmpFirstName',
        'txtEmpMiddleName',
        'txtEmpLastName',
        'txtEmployeeId',
        'txtOtherID',
        'txtLicenNo',
        'txtLicExpDate',
        'txtNICNo',
        'txtSINNo',
        'cmbMarital',
        'cmbNation',
        'DOB',
        'txtEmpNickName'}

    def __init__(self, base_url="http://hrm-online.portnov.com/symfony/web/index.php"):
        self.url = base_url
        self.sess = requests.Session()
        self.sess.headers.update(
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 " +
                           "(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"})

    def login(self, username='admin', password='password'):
        login_uri = "/auth/login"
        resp = self.sess.get(self.url + login_uri)
        token = self.extract_token(resp)

        authenticate_uri = '/auth/validateCredentials'
        login_data = {
            '_csrf_token': token,
            'txtUsername': username,
            'txtPassword': password
        }

        return self.sess.post(self.url + authenticate_uri, data=login_data)

    def add_employee(self, emp_id, first_name, last_name, middle_name='', img_file=None):
        return self.add_employee_from_json({
            'firstName': first_name,
            'middleName': middle_name,
            'lastName': last_name,
            'employeeId': str(emp_id),
            'empNumber': str(emp_id)
        }, img_file)

    def add_employee_from_json(self, emp_data, img_file):
        add_emp_uri = "/pim/addEmployee"
        resp = self.sess.get(self.url + add_emp_uri)
        token = self.extract_token(resp)
        emp_data['_csrf_token'] = token
        resp = self.sess.post(self.url + add_emp_uri,
                              files={
                                  'photofile': ('ph.jpg', open(os.path.basename(img_file), 'rb'))} if img_file else {},
                              data=emp_data)
        return resp

    @staticmethod
    def extract_token(resp, csrf_name='_csrf_token'):
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': csrf_name})['value']
        return token

    def edit_employee(self, emp_id, changed_data):
        emp_data = self.extract_employee_data(emp_id)
        for (key, val) in changed_data.items():
            emp_data[key] = val
        change_emp_uri = self.url + "/pim/viewPersonalDetails"
        return self.sess.post(change_emp_uri, files=dict(foo='bar'), data=emp_data)

    def get_employee_details(self, emp_id):
        """ Takes emp_id as a number, string, or as full / partial url """
        num_id = str(emp_id) if str(emp_id).isdigit() else None
        if not num_id:
            match = re.match(r'.*/(\d+)', emp_id)
            num_id = match.group(1) if match else None
        return self.sess.get(self.url + '/pim/viewPersonalDetails/empNumber/' + num_id)

    def add_candidate(self, first_name, last_name, email, resume):
        add_candidate_uri = "/recruitment/addCandidate/id/"
        resp = self.sess.get(self.url + add_candidate_uri)
        token = self.extract_token(resp, 'addCandidate[_csrf_token]')
        file_name = os.path.basename(resume)
        fields = {
            'addCandidate[_csrf_token]': token,
            'addCandidate[firstName]': first_name,
            'addCandidate[lastName]': last_name,
            'addCandidate[resume]': (file_name, open(resume, 'rb'), 'text/plain'),
            'addCandidate[appliedDate]': '05-27-2020',
            'addCandidate[email]': email
        }

        return self.sess.post(self.url + add_candidate_uri, data=fields, files={'foo': 'bar'})

    def extract_employee_data(self, emp_id):
        emp_response = self.get_employee_details(emp_id)
        soup = bs4.BeautifulSoup(emp_response.content, 'html5lib')
        f_name = 'personal[{0}]'
        f_id = 'personal_{0}'
        emp_data = {f_name.format('txtEmpID'): emp_id}

        for field_name in self.FIELD_NAMES:
            field_data = soup.find(id=f_id.format(field_name)).get('value', '')
            emp_data[f_name.format(field_name)] = field_data
        return emp_data

    def close(self):
        self.sess.close()
