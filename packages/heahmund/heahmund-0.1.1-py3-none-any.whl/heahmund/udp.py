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

import socket

from heahmund.logger import Logger
from heahmund.status import Status


class UDP:
    """UDP Check"""

    def __init__(self, name, hostname="example.com", port=443, timeout=30):
        self.name = name
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.logger = Logger().get_logger(__name__)

    def run(self):
        """
        Run The Check

        Returns:
            The Check Result
        """

        status = Status.OK
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        try:
            sock.sendto(b"ping", (self.hostname, self.port))

            self.logger.debug(
                "Server with hostname {} with port {}.".format(self.hostname, self.port)
            )

            status = Status.OK

        except socket.timeout:
            self.logger.debug(
                "Server with hostname {} with port {} timeout error.".format(
                    self.hostname, self.port
                )
            )

            status = Status.NOT_OK

        except socket.error as e:
            self.logger.debug(
                "Server with hostname {} with port {} error raised {}.".format(
                    self.hostname, self.port, str(e)
                )
            )

            status = Status.ERROR

        finally:
            sock.close()

        return {"name": self.name, "status": status}
