# --*--coding:utf8--*--

import cgi
import functools

from application.backend.register import AlreadyConfirmError
from application.backend.register import RegisterHelper
from application.backend.register import FakeConfirmURLError
from application.utility.json_result import  FormValidateResult
from application.utility.jsonify import jsonify
from application.utility.render_template import render_index
from application.utility.render_template import render_inform


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
        return RegisterHelper.validate_email(email)

    @check_field(NAME_FIELD)
    def check_name(self, name):
        return RegisterHelper.validate_name(name)

    def register(self):
        form = cgi.FieldStorage()
        if (EMAIL_FIELD not in form or
                NAME_FIELD not in form or
                PASSWD_FIELD not in form):
            return render_inform("Error request", 'Error request')
        else:
            email = form.getvalue(EMAIL_FIELD)
            name = form.getvalue(NAME_FIELD)
            passwd = form.getvalue(PASSWD_FIELD)
            RegisterHelper.store_to_database(email, name, passwd)
            RegisterHelper.send_confirm_email(email)
            return render_inform(
                "Please Confirm",
                'Welcome! Thanks for  signing up. \
                Please login your email to activate your account.'
                )

    def confirm_email(self):
        URL = 'url'
        form = cgi.FieldStorage()
        if URL not in form:
            return render_inform('Error', 'invalid confirm link')
        else:
            url = form.getvalue(URL)
            try:
                if RegisterHelper.confirm_email(url):
                    return render_index('info',
                                        'Confirm success, please signin. :)')
            except AlreadyConfirmError:
                return render_index('info',
                                    'Already Confirmed, please signin. :)')
            except FakeConfirmURLError:
                return render_inform('Error', 'Invalid confirm link')
