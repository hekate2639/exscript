#
# Copyright (C) 2010-2017 Samuel Abels
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from builtins import object

class LoggerProxy(object):

    """
    An object that has a 1:1 relation to a Logger object in another
    process.
    """

    def __init__(self, parent, logger_id):
        """
        Constructor.

        :type  parent: multiprocessing.Connection
        :param parent: A pipe to the associated pipe handler.
        """
        self.parent = parent
        self.logger_id = logger_id

    def add_log(self, job_id, name, attempt):
        self.parent.send(('log-add', (self.logger_id, job_id, name, attempt)))
        response = self.parent.recv()
        if isinstance(response, Exception):
            raise response
        return response

    def log(self, job_id, message):
        self.parent.send(('log-message', (self.logger_id, job_id, message)))

    def log_aborted(self, job_id, exc_info):
        self.parent.send(('log-aborted', (self.logger_id, job_id, exc_info)))

    def log_succeeded(self, job_id):
        self.parent.send(('log-succeeded', (self.logger_id, job_id)))