# --*--coding:utf8--*--
"""
    Destroy the session when user signout.
"""

from application.utility.utility import render_index
from application.utility.utility import cgi_error_logging
from application.config import config
from framework.session import Session


class Signout(object):

    def __init__(self):
        pass

    def _signout_handler(self):
        sess = Session()
        sess.destory_session()  # Not matter expired or not expired
        return render_index()

    def signout(self):
        try:
            self._signout_handler()
        except Exception as err:
            cgi_error_logging(err.message,
                              verbose=config.do_verbose_err_log)
            return render_index()


if __name__ == '__main__':
    signout = Signout()
    signout.signout()
