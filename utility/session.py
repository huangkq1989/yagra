#!--*--coding:utf8--*--

import Cookie
import hashlib 
import shelve
import time
import os

from config import config


class Session(object):

    def __init__(self, cookie_path=None):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)

        if self.cookie.get('sid'):
            sid = self.cookie['sid'].value
            # Clear session cookie from other cookies
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
                errmsg =  """%s when trying to create the session directory.  \ 
                             Create it as '%s'""" % (e.strerror, 
                                                     os.path.abspath(session_dir))
                raise OSError, errmsg 

        self.data = shelve.open(self._gen_session_file_name(sid), writeback=True) 
        os.chmod(session_dir + '/sess_' + sid, 0660) 
        # Initializes the expires data 
        if not self.data.get('cookie'): 
            self.data['cookie'] = {'expires':''} 

    def close(self): 
        self.data.close() 

    def destory_session(self):
        os.remove(self._gen_session_file_name(self.cookie['sid'].value))

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
        elif isinstance(expires, int): 
            self.data['cookie']['expires'] = time.time()+expires 
            
        self.cookie['sid']['expires'] = self.data['cookie']['expires']

    def _gen_session_file_name(self, sid):
        return config.session_dir + '/sess_' + sid
