import requests


class Authenticate(object):
    def __init__(self):
        self.base_url = 'http://hrm-online.portnov.com/symfony/web/index.php'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})

    def login_page(self):
        return self.session.get(self.base_url + '/auth/login')

    def login(self, login_data):
        return self.session.post(self.base_url + '/auth/validateCredentials', data = login_data)

    def get_add_emp_page(self):
        return self.session.get(self.base_url + '/pim/addEmployee')

    def add_employee(self, emp_data):
        return self.session.post(self.base_url + '/pim/addEmployee', data=emp_data)

    def confirm_data(self, new_emp_url):
        return self.session.get(new_emp_url)

    def get_candidates(self):
        return self.session.get(self.base_url + '/recruitment/viewCandidates')

    def click_add_candidate(self):
        return self.session.get(self.base_url + '/recruitment/addCandidate')

    def add_candidate(self, addCandidate):
        return self.session.post(self.base_url + '/recruitment/addCandidate/id', data=addCandidate)


