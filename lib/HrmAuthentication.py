from urllib import response
import bs4
import requests
from faker import Faker


class HrmAuthenticate:

    def __init__ (self):
        self.url = "http://hrm-online.portnov.com/symfony/web/index.php"
        self.session = requests.Session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        )

    def login (self, username, password):
        login_uri = "/auth/login"
        # send request to get login page html
        resp = self.session.get(self.url + login_uri)

        # Step 2: extract CSRF token = login
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        # look for input with attribute name : '_csrf_token'
        result = soup.find('input', attrs={'name': '_csrf_token'})
        # csrf token in value , we get it from that attribute
        token = result['value']
        # login page (where we send post request for login)
        authenticate_uri = '/auth/validateCredentials'

        # Step 3: login, by posting credentials + CSRF token
        login_data = {
            '_csrf_token': token,
            'txtUsername': username,
            'txtPassword': password
        }
        # send request to login
        return self.session.post(self.url + authenticate_uri, data=login_data)

    # Step 4:  get the add employee page  - contains the FORM to add employee
    def add_employee (self, emp_id):
        add_emp_uri = "/pim/addEmployee"
        resp = self.session.get(self.url + add_emp_uri)
        #  Extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': '_csrf_token'})['value']

        f = Faker()

        first_name = f.first_name()
        last_name = f.last_name()

        emp_data = {
            'firstName': first_name,
            'lastName': last_name,
            'employeeId': emp_id,
            '_csrf_token': token
        }
        # Step 6: add the employee  - posting the new employee data  + CSRF token
        return self.session.post(self.url + add_emp_uri, data=emp_data)

    # Login and submit a candidate application
    def add_candidate_application (self):
        add_application_uri = self.url + '/recruitment/addCandidate'
        resp = self.session.get(add_application_uri)

        #  extract CSRF token
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        token = soup.find('input', attrs={'name': '_csrf_token'})['value']

        f = Faker()

        first_name = f.first_name()
        last_name = f.last_name()
        emp_email = f.email()

        application_data = {
            'firstName': first_name,
            'lastName': last_name,
            '_csrf_token': token,
            'emp_email': emp_email,
        }
        # add the candidate application  - posting the new app data  + CSRF token
        return self.session.post(add_application_uri, data=application_data)

    # def verify_candidate_data(self, url, emp_id):
    #     response = self.session.get(url)
    #     soup = bs4.BeautifulSoup(response.content, 'html5lib')
    #     actual_emp_id = soup.select_one('#personal_txtEmployeeId')['value']
    #     return actual_emp_id == emp_id

    def verify_candidate_data(self, url):
        return self.session.get(url)
