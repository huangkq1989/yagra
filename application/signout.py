# --*--coding:utf8--*--

from application.utility.session import Session
from application.utility.render_template import render_index
from application.utility.utility import cgi_error_logging


class Signout(object):
    VALIDE_EXTENSION = tuple('jpg jpe jpeg png gif'.split())

    def __init__(self):
        pass

    def _signout_handler(self):
        sess = Session(cookie_path='/')
        sess.destory_session()  # Not matter expired or not expired
        return render_index()

    def signout(self):
        try:
            self._signout_handler()
        except Exception as err:
            cgi_error_logging(err.message)
            return render_index()


if __name__ == '__main__':
    signout = Signout()
    signout.signout()
