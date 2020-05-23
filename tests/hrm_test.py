import unittest

import bs4 as bs4
import requests


class HRMTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'http://hrm-online.portnov.com/symfony/web/index.php/auth'
        self.sess = requests.Session() #can use either case of session, uppercase is better
        self.sess.headers.update({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})

    def test_create_employee(self):
        login_uri = '/login'
        resp = self.sess.get(self.url + login_uri)
        soup = bs4.BeautifulSoup(resp.content, 'html5lib')
        result = soup.find('input', attrs={'name': '_csrf_token'})
        token = result['value']

        authenticate_uri = '/validateCredentials'

        login_data = {'_csrf_token': token,
                        'txtUsername': 'admin',
                        'txtPassword': 'password'
                        }
        resp = self.sess.post(self.url)


if __name__ == '__main__':
    unittest.main()
