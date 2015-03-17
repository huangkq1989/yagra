# --*--coding:utf8--*--

import sys
import os
import unittest

os.environ['DOCUMENT_ROOT'] = '/var/www/yagra/'
os.environ['REQUEST_ROOT'] = '/yagra/app.py'
sys.path.append(os.environ['DOCUMENT_ROOT'])

from application.utility.render_template import *


class RenderTemplateTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_render_template(self):
        render_template('register.html', info='hi', img='hhhhhhhh')
        pass

    def tearDown(self):
        pass


if __name__=='__main__':
    unittest.main()

