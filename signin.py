#!/usr/bin/python

import cgi
import cgitb
import os

from backend.signin import SignInHelper
from utility.render_template import render_template


class SignIn():
    NAME_FIELD = "name"
    PASSWD_FIELD = "passwd"

    def signin(self):
        form = cgi.FieldStorage()
        if (SignIn.NAME_FIELD not in form or 
                SignIn.PASSWD_FIELD not in form):
            return jsonify(ErrorJsonResult("field is missing"+email+name+passwd))
        else:
            name = form.getvalue(SignIn.NAME_FIELD)
            passwd = form.getvalue(SignIn.PASSWD_FIELD)
            SignInHelper.check_valid(name, passwd)
            return render_template("main.html")


signin = SignIn()
signin.signin()
