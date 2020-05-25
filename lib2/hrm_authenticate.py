import requests


class Authenticate(object):
    def __init__(self):
        self.base_url = 'http://hrm-online.portnov.com/symfony/web/index.php'
        self.sess = requests.Session()
        self.sess.headers.update({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})