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

        self._assemble_session_dir()
        self._mkdir_for_session_if_not_exists()

        self._session_file_name = self._gen_session_file_name(sid)
        self.data = shelve.open(self._session_file_name,
                                writeback=True)
        os.chmod(self._session_file_name, 0660)
        # Initializes the expires data
        if not self.data.get('cookie'):
            self.data['cookie'] = {'expires': ''}

    def close(self):
        self.data.close()

    def destory_session(self):
        if os.path.exists(self._session_file_name):
            os.remove(self._session_file_name)

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
        return self._session_dir + '/sess_' + sid

    def _assemble_session_dir(self):
        if not config.parent_dir_for_session_dir:
            self._session_dir = os.path.join(
                os.environ['DOCUMENT_ROOT'],
                config.session_dir_name
                )
        else:
            self._session_dir = os.path.join(
                config.parent_dir_for_session_dir,
                config.session_dir_name
                )

    def _mkdir_for_session_if_not_exists(self):
        if not os.path.exists(self._session_dir):
            try:
                os.mkdir(self._session_dir, 0770)
            except OSError as e:
                errmsg = """%s when trying to create the session directory.  \
                         Create it as '%s'""" % (e.strerror, self._session_dir)
                # If the HTTP(apache/nginx) user can't create it,
                # then create it manualy
                raise OSError(errmsg)
