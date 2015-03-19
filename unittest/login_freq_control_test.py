# --*--coding:utf8--*--
'''
    UnitTest for frequency control of error signin.
    Using mutliple processes to test concurrency is correct or not.
'''

import sys
import os
import unittest

def mock_environment():
    os.environ['DOCUMENT_ROOT'] = '/var/www/yagra/'
    sys.path.append(os.environ['DOCUMENT_ROOT'])
    os.environ['HTTP_HOST'] = 'whatever'
    os.environ['REQUEST_ROOT'] = 'whatever'
mock_environment()

from multiprocessing import Process, Pipe

from application.backend.signin import SigninHelper
from application.backend.signin import TryTooMuchError


class FreqControlTestCase(unittest.TestCase):
    def setUp(self):
        processes = []
        self.results = []
        for i in xrange(100):
            parent_conn, child_conn = Pipe()
            p = Process(target=self.request, args=(child_conn, 'huangkq',))
            p.start()
            processes.append((parent_conn, p))
        for pp, p in processes:
            result = pp.recv()
            self.results.append(result)
        for pp, p in processes:
            p.join()

    def test_freq_contral(self):
        print self.results
        l = len(filter(None, self.results))
        self.assertTrue(l == SigninHelper.THRESHOLD)

    def request(self, conn, name):
        result = None
        try:
            SigninHelper.check_frequency(name)
        except TryTooMuchError:
            result = False
        else:
            result = True
        conn.send(result)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
