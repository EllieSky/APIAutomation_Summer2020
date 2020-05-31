from lib.recruit_career.authentication import Authenticate
from lib.recruit_career.base import BaseClient
from lib.recruit_career.candidates import Candidates
from lib.recruit_career.positions import Positions


class RecruitClient(BaseClient):
    def __init__(self, client=None):
        super().__init__(client)

        self.candidate = Candidates(self)
        self.authentication = Authenticate(self)
        self.positions = Positions(self)