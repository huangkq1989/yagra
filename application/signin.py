# --*--coding:utf8--*--

import cgi
import os

from application.backend.signin import SigninHelper
from application.backend.signin import TryTooMuchError
from application.backend.signin import NeedConfirmException
from application.backend.signin import ValidUserError
from application.config import config
from application.utility.session import Session
from application.utility.render_template import render_template
from application.utility.render_template import render_index
from application.utility.render_template import render_inform


class Signin():
    NAME_FIELD = "name"
    PASSWD_FIELD = "passwd"

    def signin(self):
        form = cgi.FieldStorage()
        if (Signin.NAME_FIELD not in form or
                Signin.PASSWD_FIELD not in form):
            return render_inform("Error request", 'Error request')
        else:
            name = form.getvalue(Signin.NAME_FIELD)
            passwd = form.getvalue(Signin.PASSWD_FIELD)

            try:
                id, avatar_url = SigninHelper.check_valid(name, passwd)
                sess = Session(cookie_path='/')
                sess.data['id'] = id
                sess.set_expires(config.session_expires_interval)
                print sess.get_cookie_output()
                sess.close()
                if not avatar_url:
                    avatar_url = config.default_avatar_url
                else:
                    avatar_url = os.path.sep.join([config.avatar_request_path,
                                                   avatar_url
                                                   ])
                INFO_STR = "Support %s format." % str(config.VALIDE_EXTENSION)
                return render_template("main.html",
                                       user=cgi.escape(name, quote=True),
                                       img=avatar_url, alert_type="info",
                                       info=INFO_STR)
            except TryTooMuchError:
                return render_index('danger', 'You have tried too much!')
            except ValidUserError as err:
                ERROR_TIP = 'Password or username is wrong'
                if 0 < err.allowance:
                    ERROR_TIP = ERROR_TIP + ",   %s chances left to try"
                    ERROR_TIP = ERROR_TIP % err.allowance
                elif 0 == err.allowance:
                    ERROR_TIP = ERROR_TIP + ",  please try it after %s minutes"
                    ERROR_TIP = ERROR_TIP % (
                        SigninHelper.FORBIDDEN_INERVAL / 60)
                return render_index('danger', ERROR_TIP)
            except NeedConfirmException:
                return render_index('danger', 'Please confirm first')


if __name__ == '__main__':
    signin = Signin()
    signin.signin()
