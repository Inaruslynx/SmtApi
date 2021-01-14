from typing import Tuple
import requests
import session
import exceptions

class SmtApi(object):

    def __init__(self, user:str, pwd:str, cert:Tuple, esiid, host='https://services.smartmetertexas.net') -> None:
        super().__init__()
        ####################
        # may not need to retain
        ####################
        self.user = user
        self.pwd = pwd
        ####################
        self.url=host
        self.esiid=esiid
        # Initialize the session.
        self.session=SmtApiSession()
        self.session.init_basic_auth(user, pwd, cert)

    # Perform an API request.
    def _request(self, method, params=None, id=0):
        data = {
            'trans_id': id,
            'requestorID': self.user,
            'requesterType': 'RES',
            'version': 'L'
            'esiid': self.esiid,
            'SMTTermsandConditions': 'Y'
        }
        if params:
            data['params'] = params

        # Ask the session to perform a JSON-RPC request 
        # with the parameters provided.
        resp = self.session.request('POST', self.url, json=data)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            handle_error_response(resp)

        # Otherwise return the result dictionary.
        return resp.json()['result']

    # API methods
    # all methods require 'startDate' and 'endDate'

    def chain_head(self, chain_id):
        return self._request('chain-head', {
            'chainid': chain_id
        })

    def commit_chain(self, message):
        return self._request('commit-chain', {
            'message': message
        })

    def commit_entry(self, message):
        return self._request('commit-entry', {
            'message': message
        })
    