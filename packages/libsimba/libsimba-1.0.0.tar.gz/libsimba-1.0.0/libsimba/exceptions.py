#  Copyright (c) 2023 SIMBA Chain Inc. https://simbachain.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


UNKNOWN_EXCEPTION = "UNKNOWN ERROR"
SIMBA_INVALID_URL_EXCEPTION = "INVALID URL ERROR"
SIMBA_REQUEST_EXCEPTION = "REQUEST ERROR"
SIMBA_WALLET_EXCEPTION = "WALLET ERROR"
SIMBA_SIGNING_EXCEPTION = "SIGNING ERROR"


class LibSimbaException(Exception):
    def __init__(self, error: str = UNKNOWN_EXCEPTION, message: str = ""):
        self.error = error
        self.message = message or "Details unavailable"
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.error}: {self.message}"

    def __repr__(self) -> str:
        return self.__str__()


class SimbaInvalidURLException(LibSimbaException):
    def __init__(self, message: str = ""):
        super().__init__(error=SIMBA_INVALID_URL_EXCEPTION, message=message)


class SimbaRequestException(LibSimbaException):
    def __init__(self, message: str = ""):
        super().__init__(error=SIMBA_REQUEST_EXCEPTION, message=message)


class SimbaSigningException(LibSimbaException):
    def __init__(self, message: str = ""):
        super().__init__(error=SIMBA_SIGNING_EXCEPTION, message=message)


class SimbaWalletException(LibSimbaException):
    def __init__(self, message: str = ""):
        super().__init__(error=SIMBA_WALLET_EXCEPTION, message=message)
