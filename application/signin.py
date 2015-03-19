# --*--coding:utf8--*--
"""
    Use username and password to signin, check user error login
    frequency. After login, establish a session, set a cookie
    to the user. Then will response user's avatar if he has uploaded,
    or responses a default avatar.
"""

import cgi
import time

from application.backend.signin import SigninHelper
from application.backend.signin import TryTooMuchError
from application.backend.signin import NeedConfirmException
from application.backend.signin import ValidUserError
from application.config import config
from application.utility import feedback_msg as msg
from application.utility.utility import get_default_avatar_request_url
from application.utility.utility import get_request_url_for_avatar
from application.utility.utility import render_index
from application.upload import Upload
from framework.render_template import render_template
from framework.session import Session


class Signin():
    NAME_FIELD = "name"
    PASSWD_FIELD = "passwd"

    def _get_invalid_user_feedback(self, err):
        error_tip = msg.SIGNIN_INVALID_NAME_OR_PW
        if 0 < err.allowance:
            error_tip = ', '.join([error_tip, msg.SIGNIN_CHANCE_LEFT])
            error_tip = error_tip % err.allowance
        elif 0 == err.allowance:
            error_tip = ', '.join([error_tip, msg.SIGNIN_TRY_IT_LATER])
            error_tip = error_tip % (
                SigninHelper.FORBIDDEN_INERVAL / 60)
        return error_tip

    def _assemble_one_session(self, id):
        sess = None
        try:
            sess = Session(cookie_path='/')
            sess.data['id'] = id
            sess.set_expires(config.session_expires_interval)
            sess.set_cookie_to_respone()
        finally:
            if sess:
                sess.close()

    def signin(self):
        form = cgi.FieldStorage()
        if (Signin.NAME_FIELD not in form or
                Signin.PASSWD_FIELD not in form):
            return render_index(msg.SIGNIN_ALERT_TYPE_INFO,
                                msg.SIGNIN_MSG_WELCOME)
        else:
            name = form.getvalue(Signin.NAME_FIELD)
            passwd = form.getvalue(Signin.PASSWD_FIELD)

            try:
                id, avatar_url_in_db = SigninHelper.check_valid(name, passwd)

                self._assemble_one_session(id)

                if not avatar_url_in_db:  # Didn't upload a avatar yet.
                    avatar_url = get_default_avatar_request_url()
                else:
                    avatar_url = get_request_url_for_avatar(avatar_url_in_db)

                # Append a timestamp to disable browser cached.
                avatar_url = '?'.join([avatar_url, str(time.time())])
                info_str = msg.UPLOAD_TIP % (str(config.valid_extension),
                                             (Upload.LIMIT_SIZE / 1024))
                return render_template("main.html",
                                       user=cgi.escape(name, quote=True),
                                       img=avatar_url,
                                       info=info_str)
            except TryTooMuchError as err:
                return render_index(msg.SIGNIN_ALERT_TYPE_DANGER,
                                    err.message)
            except ValidUserError as err:
                error_tip = self._get_invalid_user_feedback(err)
                return render_index(msg.SIGNIN_ALERT_TYPE_DANGER,
                                    error_tip)
            except NeedConfirmException as err:
                return render_index(msg.SIGNIN_ALERT_TYPE_DANGER, err.message)


if __name__ == '__main__':
    signin = Signin()
    signin.signin()
