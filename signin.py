#!/usr/local/bin/python2.7

import cgi
import cgitb
import os
import sys

from backend.signin import SignInHelper
from config import config
from utility.jsonify import jsonify
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
                result, session = SignInHelper.check_valid(name, passwd)
                if result:
                    headers = {}
                    headers['Set-Cookie'] = 'sid=%s;' % session.cookie['sid'].value
                    print_headers(headers)
                    return render_template("main.html", 
                                           img=config.default_avatar_url)
                else:
                    return render_inform("Wrong", 'password or username is wrong')
            except Exception as err:
                return render_inform("Wrong Happened", 'Please try it Again')


            return jsonify(ErrorJsonResult("password or username is wrong"))


signin = SignIn()
signin.signin()
