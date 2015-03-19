# --*--coding:utf8--*--
"""
    Bussiness Logic for registartion. Email, username and password
    are required, which email and username must be unique.

    After user submits the form, will send a confirm email to user,
    when user clicks the confirm email, registration is done.
"""

import cgi
import functools
import sys

from application.utility.confirm_url_serializer import AlreadyConfirmError
from application.utility.confirm_url_serializer import FakeConfirmURLError
from application.utility.confirm_url_serializer import TimedOutURLError
from application.utility.json_result import FormValidateResult
from application.backend.register import RegisterHelper
from application.utility import feedback_msg as msg
from application.utility.utility import render_index
from application.utility.utility import render_inform
from framework.jsonify import jsonify
from framework.render_template import render_template


def check_field(field_name):
    def decoder(is_valid_field):
        @functools.wraps(is_valid_field)
        def _check_field(instance):
            form = cgi.FieldStorage()
            field_value = form.getvalue(field_name)
            if field_name not in form:
                return jsonify(FormValidateResult(False))
            elif is_valid_field(instance, field_value):
                return jsonify(FormValidateResult(True))
            else:
                return jsonify(FormValidateResult(False))
        return _check_field
    return decoder


EMAIL_FIELD = "email"
NAME_FIELD = "name"
PASSWD_FIELD = "passwd"


class Register(object):

    @check_field(EMAIL_FIELD)
    def check_email(self, email):
        '''Check email is still avariable or not.'''
        return RegisterHelper.validate_email(email)

    @check_field(NAME_FIELD)
    def check_name(self, name):
        '''Check user name is still avariable or not.'''
        return RegisterHelper.validate_name(name)

    def register(self):
        '''Handle registration by insert to database
        and send a comfirm email.
        '''

        form = cgi.FieldStorage()
        if (EMAIL_FIELD not in form or
                NAME_FIELD not in form or
                PASSWD_FIELD not in form):
            return render_template('register.html')
        else:
            email = form.getvalue(EMAIL_FIELD)
            name = form.getvalue(NAME_FIELD)
            passwd = form.getvalue(PASSWD_FIELD)
            RegisterHelper.store_to_database(email, name, passwd)
            try:
                RegisterHelper.send_confirm_email(email)
                return render_inform(msg.INFORM_TITLE_NEED_CONFIRM,
                                     msg.INFORM_MSG_NEED_CONTIRM)
            except Exception as err:
                RegisterHelper.rollback_record(email)
                (exc, exc_type, tb) = sys.exc_info()
                raise err, None, tb

    def confirm_email(self):
        '''Check confirm request is valid or not.'''
        URL = 'url'
        form = cgi.FieldStorage()
        try:
            if URL not in form:
                raise FakeConfirmURLError()
            url = form.getvalue(URL)

            if RegisterHelper.check_confirm_link(url):
                return render_index(msg.SIGNIN_ALERT_TYPE_INFO,
                                    msg.SIGNIN_MSG_CONFIRM_SUCCESS)
        except AlreadyConfirmError as err:
            return render_index(msg.SIGNIN_ALERT_TYPE_DANGER, err.message)
        except FakeConfirmURLError as err:
            return render_inform(msg.INFORM_TITLE_ERROR, err.message)
        except TimedOutURLError as err:
            return render_inform(msg.INFORM_TITLE_ERROR, err.message)
