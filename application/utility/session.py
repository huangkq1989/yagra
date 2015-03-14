#!--*--coding:utf8--*--

import Cookie
import hashlib
import shelve
import time
import os

from application.config import config


class Session(object):

    def __init__(self, cookie_path=None):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)

        if self.cookie.get('sid'):
            sid = self.cookie['sid'].value
            # Clear session cookie from application.other cookies
            self.cookie.clear()
        else:
            self.cookie.clear()
            sid = hashlib.md5(repr(time.time())).hexdigest()
        self.cookie['sid'] = sid

        if cookie_path:
            self.cookie['sid']['path'] = cookie_path

        session_dir = config.session_dir
        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 0770)
                # If the apache user can't create it create it manualy
            except OSError, e:
                errmsg = """%s when trying to create the session directory.  \
                         Create it as '%s'""" % (e.strerror,
                                                 os.path.abspath(session_dir))
                raise OSError(errmsg)

        self.data = shelve.open(self._gen_session_file_name(sid),
                                writeback=True)
        os.chmod(session_dir + '/sess_' + sid, 0660)
        # Initializes the expires data
        if not self.data.get('cookie'):
            self.data['cookie'] = {'expires': ''}

    def close(self):
        self.data.close()

    def destory_session(self):
        os.remove(self._gen_session_file_name(self.cookie['sid'].value))

    def get_cookie_output(self):
        return self.cookie.output()

    def is_expired(self, next_expires):
        expire_time = self.data['cookie']['expires']
        if expire_time < time.time():
            self.destory_session()
            return True
        else:
            self.set_expires(next_expires)
            return False

    def set_expires(self, expires=None):
        if expires == '':
            self.data['cookie']['expires'] = ''
            self.cookie['sid']['expires'] = ''
        elif isinstance(expires, int):
            self.data['cookie']['expires'] = time.time() + expires
            loc_time = time.localtime(self.data['cookie']['expires'])
            expired_time = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", loc_time)
            self.cookie['sid']['expires'] = expired_time

    def _gen_session_file_name(self, sid):
        return config.session_dir + '/sess_' + sid


class SessionCleaner(object):
    """Use to remove session file in case of client
    exits session undeservedly.
    """
    def __init__(self):
        self._run_interval = 60 * 60 * 5

    def loop(self):
        pass


if __name__ == '__main__':
    cleaner = SessionCleaner()
    cleaner.loop()
