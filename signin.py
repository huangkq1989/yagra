#!/usr/local/bin/python2.7

import cgi
import cgitb
import os
import sys

from backend.signin import SignInHelper
from config import config
from utility.session import Session
from utility.render_template import print_headers
from utility.render_template import render_template
from utility.render_template import render_inform
from utility.json_result import JsonResult
from utility.json_result import ErrorJsonResult


cgitb.enable()


class SignIn():
    NAME_FIELD = "name"
    PASSWD_FIELD = "passwd"

    def signin(self):
        form = cgi.FieldStorage()
        if (SignIn.NAME_FIELD not in form or 
                SignIn.PASSWD_FIELD not in form):
            return render_inform("Error request", 'Error request')
        else:
            try:
                name = form.getvalue(SignIn.NAME_FIELD)
                passwd = form.getvalue(SignIn.PASSWD_FIELD)
                result, id, avatar_url = SignInHelper.check_valid(name, 
                                                                       passwd)
                if result:

                    sess = Session(cookie_path='/')
                    sess.data['id'] = id 
                    headers = {}
                    headers['Set-Cookie'] = 'sid=%s;' % sess.cookie['sid'].value
                    sess.set_expires(config.session_expires_interval)
                    sess.close()
                    print_headers(headers)
                    avatar_url = os.path.sep.join([config.avatar_request_path, 
                                                   avatar_url
                                                   ]) 
                    return render_template("main.html", img=avatar_url)
                else:
                    return render_inform("Wrong", 'password or username is wrong')
            except Exception as err:
                return render_inform("Wrong Happened", 'Please try it Again')


signin = SignIn()
signin.signin()
