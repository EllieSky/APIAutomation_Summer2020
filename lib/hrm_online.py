from io import StringIO

import bs4
from dateutil.utils import today
from faker import Faker
from requests import Session


class HrmOnline(object):
    def __init__(self, base_url='http://hrm-online.portnov.com/symfony/web/index.php'):
        self.url = base_url
        self.sess = Session()
        self.sess.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 '
                          'Safari/537.36'}
        )
        self.faker = Faker()

    def login(self, username, password):
        login_uri = "/auth/login"
        resp = self.sess.get(self.url + login_uri)
        token = self.extract_token(resp)
        authenticate_uri = '/auth/validateCredentials'
        login_data = {
            '_csrf_token': token,
            'txtUsername': username,
            'txtPassword': password
        }
        resp = self.sess.post(self.url + authenticate_uri, data=login_data)
        return resp

    def add_emp(self, emp_data):
        uri = '/pim/addEmployee'
        resp = self.sess.get(self.url + uri)
        token = self.extract_token(resp)
        emp_data['_csrf_token'] = token
        resp = self.sess.post(self.url + uri, data=emp_data)
        return resp

    def extract_emp_id(self, resp):
        resp = self.sess.get(resp.url)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']
        return actual_emp_id

    def add_candidate(self, cand_data):
        uri = '/recruitment/addCandidate'
        resp = self.sess.get(self.url + uri)
        token = self.extract_token(resp, 'addCandidate[_csrf_token]')
        cand_json = cand_data.copy()
        cand_json['addCandidate[_csrf_token]'] = token
        resp = self.sess.post(self.url + uri, files={'addCandidate[resume]': ('', StringIO(''), 'application/octet'
                                                                                                '-stream')},
                              data=cand_json)
        return resp

    @staticmethod
    def extract_token(resp, name='_csrf_token'):
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': name})
        return result['value']

    def generate_emp_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        emp_id = self.faker.random_number(6)
        emp_data = {
            'firstName': first_name,
            'lastName': last_name,
            'employeeId': emp_id,
        }
        return emp_data

    def generate_cand_data(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.email()
        cand_data = {
            'addCandidate[firstName]': first_name,
            'addCandidate[middleName]': '',
            'addCandidate[lastName]': last_name,
            'addCandidate[email]': email,
            'addCandidate[contactNo]': '',
            'addCandidate[vacancy]': '',
            'addCandidate[keyWords]': '',
            'addCandidate[comment]': '',
            'addCandidate[appliedDate]': today().strftime('%m-%d-%Y')
        }
        return cand_data

    @staticmethod
    def extract_cand_data(resp):
        bs = bs4.BeautifulSoup(resp.content, 'html5lib')
        cand_data = {
            'addCandidate[firstName]': get_input(bs, 'addCandidate[firstName]'),
            'addCandidate[middleName]': get_input(bs, 'addCandidate[middleName]'),
            'addCandidate[lastName]': get_input(bs, 'addCandidate[lastName]'),
            'addCandidate[email]': get_input(bs, 'addCandidate[email]'),
            'addCandidate[contactNo]': get_input(bs, 'addCandidate[contactNo]'),
            'addCandidate[keyWords]': get_input(bs, 'addCandidate[keyWords]'),
            'addCandidate[appliedDate]': get_input(bs, 'addCandidate[appliedDate]'),
            'addCandidate[comment]': bs.find(id='addCandidate_comment').text,
            'addCandidate[vacancy]': bs.find('option', attrs={'selected': 'selected'}).get('value', '')
        }
        return cand_data


def get_input(soup, name):
    return soup.find('input', attrs={'name': name})['value']
