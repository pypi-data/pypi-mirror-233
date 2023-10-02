# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
from http import HTTPStatus

from heahmund.status import Status
from heahmund.logger import Logger


class GET:
    """GET Check"""

    def __init__(self, name, url, headers={}, params={}):
        self.name = name
        self.url = url
        self.headers = headers
        self.params = params
        self.logger = Logger().get_logger(__name__)

    def run(self):
        """
        Run The Check

        Returns:
            The Check Result
        """

        try:
            response = requests.get(self.url, headers=self.headers, params=self.params)

            if response.status_code == HTTPStatus.OK:
                return {"name": self.name, "status": Status.OK}
            else:
                return {"name": self.name, "status": Status.NOT_OK}

        except requests.exceptions.Timeout as e:
            self.logger.debug(
                "Get request to url {} throw timeout error {}.".format(self.url, str(e))
            )

            return {"name": self.name, "status": Status.ERROR}

        except Exception as e:
            self.logger.debug(
                "Get request to url {} throw error {}.".format(self.url, str(e))
            )

            return {"name": self.name, "status": Status.ERROR}


class HEAD:
    """HEAD Check"""

    def __init__(self, name, url, headers={}, params={}):
        self.name = name
        self.url = url
        self.headers = headers
        self.params = params
        self.logger = Logger().get_logger(__name__)

    def run(self):
        """
        Run The Check

        Returns:
            The Check Result
        """

        try:
            response = requests.head(self.url, headers=self.headers, params=self.params)

            if response.status_code == HTTPStatus.OK:
                return {"name": self.name, "status": Status.OK}
            else:
                return {"name": self.name, "status": Status.NOT_OK}

        except requests.exceptions.Timeout as e:
            self.logger.debug(
                "Get request to url {} throw timeout error {}.".format(self.url, str(e))
            )

            return {"name": self.name, "status": Status.ERROR}

        except Exception as e:
            self.logger.debug(
                "Get request to url {} throw error {}.".format(self.url, str(e))
            )

            return {"name": self.name, "status": Status.ERROR}
