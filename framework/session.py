#!--*--coding:utf8--*--
'''
    Session Management. 
'''

import Cookie
import hashlib
import shelve
import time
import os

from application.config import config


class ExpiredNotSetException(Exception):
    pass


class InvalidExpiredType(Exception):
    pass


class Session(object):
    '''Session Management. Use shelve store session info.'''

    def __init__(self, cookie_path=None):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)

        if self.cookie.get('sid'):
            sid = self.cookie['sid'].value
            self.cookie.clear()
        else:
            self.cookie.clear()
            sid = hashlib.md5(repr(time.time()) +
                              config.session_salt
                              ).hexdigest()
        self.cookie['sid'] = sid

        if cookie_path:
            self.cookie['sid']['path'] = cookie_path

        self._mkdir_for_session_if_not_exists(config.session_dir)

        self.data = shelve.open(self._gen_session_file_name(sid),
                                writeback=True)
        os.chmod(config.session_dir + '/sess_' + sid, 0660)
        # Initializes the expires data
        if not self.data.get('cookie'):
            self.data['cookie'] = {'expires': ''}

    def close(self):
        self.data.close()

    def destory_session(self):
        session_file = self._gen_session_file_name(self.cookie['sid'].value)
        if os.path.exists(session_file):
            os.remove(session_file)

    def set_cookie_to_respone(self):
        print self.cookie.output()

    def is_expired(self, next_expires):
        expire_time = self.data['cookie']['expires']
        if isinstance(expire_time, int):
            raise ExpiredNotSetException()

        if expire_time < time.time():
            self.destory_session()
            return True
        else:
            self.set_expires(next_expires)
            return False

    def set_expires(self, expires=None):
        if isinstance(expires, int):
            self.data['cookie']['expires'] = time.time() + expires
            loc_time = time.localtime(self.data['cookie']['expires'])
            expired_time = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", loc_time)
            self.cookie['sid']['expires'] = expired_time
        else:
            raise InvalidExpiredType()

    def _gen_session_file_name(self, sid):
        return config.session_dir + '/sess_' + sid

    def _mkdir_for_session_if_not_exists(self, session_dir):

        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 0770)
            except OSError, e:
                errmsg = """%s when trying to create the session directory.  \
                         Create it as '%s'""" % (e.strerror,
                                                 os.path.abspath(session_dir))
                # If the HTTP(apache/nginx) user can't create it,
                # then create it manualy
                raise OSError(errmsg)
