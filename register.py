#!/usr/local/bin/python2.7

import cgi
import cgitb
import os
import json

from backend.register import AlreadyConfirmError
from backend.register import RegisterHelper
from backend.register import FakeConfirmURLError
from utility.jsonify import FormValidateResult
from utility.jsonify import jsonify
from utility.render_template import render_template
from utility.render_template import render_inform

cgitb.enable()


EMAIL_FIELD = "email"
NAME_FIELD = "name"
PASSWD_FIELD = "passwd"


def check_field(field_name):
    def decoder(is_valid_field):
        def _check_field():
            form = cgi.FieldStorage() 
            field_value = form.getvalue(field_name)
            if field_name not in form:
                return jsonify(FormValidateResult(False)) 
            elif is_valid_field(field_value):
                return jsonify(FormValidateResult(True)) 
            else:
                return jsonify(FormValidateResult(False)) 
        return _check_field
    return decoder


@check_field(EMAIL_FIELD)
def check_email(email):
    return RegisterHelper.validate_email(email)


@check_field(NAME_FIELD)
def check_name(name):
    return RegisterHelper.validate_name(name)


def register():
    form = cgi.FieldStorage() 
    if (EMAIL_FIELD not in form or 
            NAME_FIELD not in form or 
            PASSWD_FIELD not in form):
        return render_inform("Error request", 'Error request')
    else: 
        try:
            email = form.getvalue(EMAIL_FIELD)
            name = form.getvalue(NAME_FIELD)
            passwd = form.getvalue(PASSWD_FIELD)
            RegisterHelper.store_to_database(email, name, passwd)
            RegisterHelper.send_confirm_email(email)
        except Exception as err:
            return render_inform("Wrong Happened", 'Please try it Again')
        return render_inform(
                "Please Confirm", 
                'Welcome! Thanks for  signing up. \
                Please login your email to activate your account.'
                )


def confirm_email():
    URL = 'url'
    form = cgi.FieldStorage() 
    if URL not in form:
        return render_inform('Error', 'invalid confirm link')
    else:
        url = form.getvalue(URL)
        try:
            if RegisterHelper.confirm_email(url):
                return render_template("signin.html", info='Confirm success, please signin:)' )
        except AlreadyConfirmError as err:
            return render_inform('Error', 'Already confirmed')
        except FakeConfirmURLError as err:
            return render_inform('Error', 'Invalid confirm link')



def route():
    route_map = {'check_email': check_email,
                 'check_name': check_name,
                 'register': register,
                 'confirm': confirm_email,
                 }
    try:
        route_map[os.environ['PATH_INFO'][1:]]()
    except KeyError as err:
        return render_inform("Error 404", "Page Not Found")
    except Exception as err:
        return render_inform("Error", "Please try it again")


route()
