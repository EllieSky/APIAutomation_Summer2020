import unittest
import bs4
from requests import Session
from  faker import Faker


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


if __name__ == '__main__':
    unittest.main()
