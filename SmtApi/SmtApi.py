""" 
Programmer: Joshua Edwards
Purpose: Provide interface with SmartMeterTexas.com. Provide a way to quickly pull meter reads and data.
 """
import datetime
import re
from typing import Mapping, Tuple, Optional
from session import SmtApiSession
from exceptions import handle_error_response


class SmtApi(object):

    def __init__(self, user: str, pwd: str, cert: Tuple[str, str], esiid: str, Test=False) -> None:
        """ 
        Instantiate a new API client.
        Args:
            user (str): username for API log in as given by SMT for API development
            pwd (str): password for API log in as given by SMT for API development
            cert (Tuple[str, str]): location to certification and key file as strings
            esiid (str): esiid associated with account a string of numbers
            Test (bool): changes host if using test API
         """
        ####################
        # may not need to retain
        ####################
        self.user = user
        self.pwd = pwd
        ####################
        if Test == True:
            self.host = 'https://uatservices.smartmetertexas.net'
        else:
            self.host = 'https://services.smartmetertexas.net'
        self.__url = ''
        self.esiid = esiid
        self.id = 0
        # Initialize the session.
        self.session = SmtApiSession()
        self.session.init_basic_auth(user, pwd, cert)

    # url property
    @property
    def url(self):
        return self.__url

    # url setter
    @url.setter
    def url(self, path: str):
        self.__url = self.host + '/{:d}/'.format(path)

    # Perform an API request.
    def _request(self, method: str, params: Mapping[str, str], type='RES', deliveryMode='XML') -> Mapping[str, str]:
        self.url = method
        # shared param off 3 defined methods
        data = {
            'trans_id': str(self.id),
            'requesterType': type,
            'requestorID': self.user,
            'deliveryMode': deliveryMode,
            'esiid': self.esiid,
            'SMTTermsandConditions': 'Y'
        }
        # params is a required argument
        data.update(params)

        # Ask the session to perform a JSON-RPC request
        # with the parameters provided.
        resp = self.session.request('POST', self.url, json=data)

        # If something goes wrong, we'll pass the response
        # off to the error-handling code
        if resp.status_code >= 400:
            handle_error_response(resp)

        # Otherwise return the result dictionary and increment id.
        self.id += 1
        # ['result'] came from example code used. I'm not sure if it's required as returning whole json seems appropriate
        return resp.json()  # ['result']

    # API methods
    # all methods require 'startDate' and 'endDate'
    # format for dates: mm/dd/yyyy
    # Available methods: 15minintervalreads (pg 18 of SmartMeterTexas pdf), dailyreads (pg 25 of SMT pdf), odr (on-demand read - pg 56 of SMT pdf)

    # 15 Minute Interval Reads (pg 18 of SmartMeterTexas pdf)

    def min_interval_reads(self, startDate: datetime, endDate: datetime, params: Optional[Mapping[str, str]] = None, ver='L', readingType='C') -> Mapping[str, list[float]]:
        """ 
        Returns 15-minute interval reads from starting date to ending date.
        """ 
        """
        1st: Format dates and test not today
        2nd: Build json
        3rd: Make request
        4th: Parse data and return as Dict[str, list] list of floats
         """
        # 1st
        # format dates as a string: mm/dd/yyyy
        today = datetime.date.today().strftime("%m/%d/%Y")
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        if today == startDate or today == endDate:
            raise ValueError('May not use today with this function')
        # 2nd
        # required params
        data = {
            'version': ver,
            'readingType': readingType,
            'startDate': startDate,  # mm/dd/yyyy str
            'endDate': endDate  # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        # 3rd
        # call _request function which will then return a json
        response = self._request('15minintervalreads', data)
        # 4th
        energyData = response['energyData']
        parsedData = {}
        days = []
        for eachday in energyData:
            days.append(eachday['DT'])
            parsedData[eachday['DT']] = eachday['RD'].rsplit(',')
        # Recommend https://pythex.org/ for testing patterns
        pattern = '[^aAeE-]'
        for eachDay in days:
            for eachReading in parsedData[eachDay]:
                eachReading = float(re.findall(pattern, eachReading))
        return parsedData

    # Daily Reads (pg 25 of SMT pdf)
    def daily_reads(self, startDate: datetime, endDate: datetime, params: Optional[Mapping[str, str]] = None, ver='L', readingType='C') -> Mapping[str, str]:
        """ 
        Returns daily reads from start date to end date
        """
        # format dates as a string: mm/dd/yyyy
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        # required params
        data = {
            'version': ver,
            'readingType': readingType,
            'startDate': startDate,  # mm/dd/yyyy str
            'endDate': endDate  # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        # call _request function which will then return a json
        return self._request('dailyreads', data)

    # On-Demand Read (pg 56 of SMT pdf)
    # This is the most complicated
    # It appears you can request up to 3,000 requests a day. After you submit a request, a read from meter will start pulling
    # so we have to wait for that pull to finish. I believe we are waiting for On-Demand Read Status
    def odr(self,  startDate: datetime, endDate: datetime, params: Optional[Mapping[str, str]] = None) -> Mapping[str, str]:
        # format dates as a string: mm/dd/yyyy
        startDate = startDate.strftime("%m/%d/%Y")
        endDate = endDate.strftime("%m/%d/%Y")
        # required params
        data = {
            'startDate': startDate,  # mm/dd/yyyy str
            'endDate': endDate  # mm/dd/yyyy str
        }
        # optional params
        if params:
            data.update(params)
        # call _request function which will then return a json
        return self._request('odr', data)

    # On-Demand Read Status
    # I don't understand documentation. It only gives an example with odrRead with a date, but no kWh reading
