import requests


class BaseClient(object):
    def __init__(self, client=None):
        self.client = client

        if client and isinstance(client, BaseClient):
            self.base_url = client.base_url
            self.session = client.session
        else:
            self.base_url = 'https://recruit-portnov.herokuapp.com/recruit/api/v1'
            self.session = requests.Session()
            self.session.headers.update({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
        )


