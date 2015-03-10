#!/usr/local/bin/python2.7

import cgi
import cgitb
import os

from backend.register import RegisterHelper
from utility.check_field import check_field
from utility.jsonify import jsonify
from utility.render_template import render_template
from utility.json_result import JsonResult
from utility.json_result import ErrorJsonResult

#cgitb.enable()


EMAIL_FIELD = "email"
NAME_FIELD = "name"
PASSWD_FIELD = "passwd"


@check_field(EMAIL_FIELD)
def check_email(self, email):
    RegisterHelper.validate_email(email)


@check_field(NAME_FIELD)
def check_name(self, name):
    RegisterHelper.validate_email(name)


def register():
    form = cgi.FieldStorage() 
    if (EMAIL_FIELD not in form or 
            NAME_FIELD not in form or 
            PASSWD_FIELD not in form):
        return jsonify(ErrorJsonResult("field is missing")) 
    else: 
        email = form.getvalue(EMAIL_FIELD)
        name = form.getvalue(NAME_FIELD)
        passwd = form.getvalue(PASSWD_FIELD)
        RegisterHelper.store_to_database(email, name, passwd)
        RegisterHelper.send_confirm_email(email)
        return render_template("confirm.html", info='Welcome! Thanks for signing up. Please login your email to activate your account.')


def confirm_email():
    URL = 'url'
    form = cgi.FieldStorage() 
    if URL not in form:
        return render_template("confirm.html", info='invalid confirm link')
    else:
        url = form.getvalue(URL)
        if RegisterHelper.confirm_email(url):
            return render_template("../../index.html")
        else:
            return render_template("confirm.html", info='invalid confirm link')


def route():
    path_info = os.environ['PATH_INFO']
    route_map = {'check_email': check_email,
                 'check_name': check_name,
                 'register': register,
                 'confirm': confirm_email,
                 }
    try:
        route_map[os.environ['PATH_INFO'][1:]]()
    except KeyError as err:
        return render_template("not_found.html")


route()
