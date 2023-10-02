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

import ssl
import datetime
import socket

from heahmund.logger import Logger
from heahmund.status import Status


class SSL:
    """SSL Check"""

    def __init__(self, name, hostname="example.com", days=10, port=443, timeout=30):
        self.name = name
        self.hostname = hostname
        self.days = days
        self.port = port
        self.timeout = timeout
        self.logger = Logger().get_logger(__name__)

    def run(self):
        """
        Run The Check

        Returns:
            The Check Result
        """

        context = ssl.create_default_context()

        try:
            # Connects to the server using the SSL context
            with socket.create_connection(
                (self.hostname, self.port), timeout=self.timeout
            ) as sock:
                sock.settimeout(self.timeout)

                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()

                    # Get the expiration date of the certificate
                    expiry_date = datetime.datetime.strptime(
                        cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
                    )

                    # Get the current date
                    current_date = datetime.datetime.now()

                    # Calculate the number of days until the certificate expires
                    days_until_expiry = (expiry_date - current_date).days

                    # Check if the certificate is valid for the specified number of days
                    if days_until_expiry > self.days:
                        return {"name": self.name, "status": Status.OK}
                    else:
                        return {"name": self.name, "status": Status.NOT_OK}

        except socket.timeout:
            # Handle the timeout
            return {"name": self.name, "status": Status.TIMEOUT}
