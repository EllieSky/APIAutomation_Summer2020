import requests

from lib.authentication import Authenticate
from lib.candidates import Candidates
from lib.positions import Positions


class BaseClient(object):
    def __init__(self, client=None):
        self.client = client
        self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
        self.session = requests.Session()
        self.session.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        )


class RecruitClient(BaseClient):
    def __init__(self, client=None):
        if client and isinstance(client, BaseClient):
            self.base_url = client.base_url
            self.session = client.session
        else:
            super.__init__(client)
        # sub clients, inherits from BaseClient
        self.authentication = Authenticate()
        self.positions = Positions()
        self.candidate = Candidates()