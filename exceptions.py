# GOAL: Handle exceptions for SmtApi.

# Take a HTTP response object and translate it into an Exception
# instance.
def handle_error_response(resp):
    # Mapping of API response codes to exception classes
    codes = {
        -1: SmtApiError,
        '400': BadRequest,
        '401': AuthFail,
        '403': HeaderMissing,
       '500': GenericError,
    }

    error = resp.json().get('error', {})
    message = error.get('errorMessage')
    code = error.get('errorCode', -1)
    data = error.get('errorKey', {})

    # Build the appropriate exception class with as much
    # data as we can pull from the API response and raise
    # it.
    raise codes[code](message=message, code=code, data=data, response=resp)


class SmtApiError(Exception):
    response = None
    data = {}
    code = -1
    message = "An unknown error occurred"

    def __init__(self, message=None, code=None, data={}, response=None):
        self.response = response
        if message:
            self.message = message
        if code:
            self.code = code
        if data:
            self.data = data

    def __str__(self):
        if self.code:
            return '{}: {}'.format(self.code, self.message)
        return self.message

# Specific exception classes

class BadRequest(SmtApiError):
    pass


class AuthFail(SmtApiError):
    pass


class HeaderMissing(SmtApiError):
  pass


class GenericError(SmtApiError):
  pass