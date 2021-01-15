import datetime
from typing import Any, Tuple, Dict, Optional
from session import SmtApiSession
from exceptions import handle_error_response


class SmtApi(object):

    def __init__(self, user: str, pwd: str, cert: Tuple[str, str], esiid: str, host='https://services.smartmetertexas.net') -> None:
        """ 
        Instantiate a new API client.
        Args:
            user (str): username for API log in
            pwd (str): password for API log in
            cert (Tuple[str, str]): location to certification and key file as strings
            esiid (str): esiid associated with account a string of numbers
            host (str): base of API to be joined to API functions
         """
        ####################
        # may not need to retain
        ####################
        self.user = user
        self.pwd = pwd
        ####################
        self.host = host
        self.esiid = esiid
        self.id = 0
        # Initialize the session.
        self.session = SmtApiSession()
        self.session.init_basic_auth(user, pwd, cert)

    # Perform an API request.
    def _request(self, method: str, params: Dict[str, str], type='RES', deliveryMode='XML') -> Any:
        url = self._url(method)
        # shared param off 3 defined methods
        data = {
            'trans_id': str(self.id),
            'requesterType': type,
            'requestorID': self.user,
            'deliveryMode': deliveryMode,
            'esiid': self.esiid,
            'SMTTermsandConditions': 'Y'
        }
        # should always have additional params
        if params:
            data.update(params)
        else:
            # TODO: error and need to handle
            pass

        # Ask the session to perform a JSON-RPC request
        # with the parameters provided.
        resp = self.session.request('POST', url, json=data)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            handle_error_response(resp)

        # Otherwise return the result dictionary and increment id.
        self.id += 1
        # ['result'] came from example code used I'm not sure if it's requires as returning whole json seems appropriate
        return resp.json()#['result']

    # url helper
    def _url(self, path):
        return self.host + '/{:d}/'.format(path)

    # API methods
    # all methods require 'startDate' and 'endDate'
    # format for dates: mm/dd/yyyy
    # Available methods: 15minintervalreads (pg 18 of SmartMeterTexas pdf), dailyreads (pg 25 of SMT pdf), odr (on-demand read - pg 56 of SMT pdf)

    # 15 Minute Interval Reads (pg 18 of SmartMeterTexas pdf)
    def min_interval_reads(self, startDate: datetime, endDate: datetime, params: Optional[Dict[str, str]] = None, ver='L', readingType='C'):
        # format dates as a string: mm/dd/yyyy
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        # required params
        data = {
            'version': ver,
            'readingType': readingType,
            'startDate': startDate, # mm/dd/yyyy str
            'endDate': endDate # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        return self._request('15minintervalreads', data)

    # Daily Reads (pg 25 of SMT pdf)
    def daily_reads(self, startDate: datetime, endDate: datetime, params: Optional[Dict[str, str]] = None, ver='L', readingType='C'):
        # format dates as a string: mm/dd/yyyy
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        # required params
        data = {
            'version': ver,
            'readingType': readingType,
            'startDate': startDate, # mm/dd/yyyy str
            'endDate': endDate # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        return self._request('dailyreads', data)

    # On-Demand Read (pg 56 of SMT pdf)
    # This is the most complicated
    # It appears you can request up to 3,000 requests a day. After you submit a request, a read from meter will start pulling
    # so we have to wait for that pull to finish. I believe we are waiting for On-Demand Read Status
    def odr(self,  startDate: datetime, endDate: datetime, params: Optional[Dict[str, str]] = None):
        # format dates as a string: mm/dd/yyyy
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        # required params
        data = {
            'startDate': startDate, # mm/dd/yyyy str
            'endDate': endDate # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        return self._request('odr', data)

    # On-Demand Read Status
    # I don't understand documentation. It only gives an example with odrRead with a date, but no kWh reading
