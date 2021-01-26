from typing import Tuple

import requests


class SmtApiSession(requests.Session):

    def __init__(self, *args, **kwargs):
        super(SmtApiSession, self).__init__(*args, **kwargs)
    
    def init_basic_auth(self, username:str, password:str, cert:Tuple):
        self.auth = (username, password)
        self.cert = cert
