# --*--coding:utf8--*--

import hashlib
import os

from application.backend.mysql_helper import get_db_cursor
from application.config import config
from application.utility.confirm_url_serializer import ConfirmURLSerializer
from application.utility.utility import send_mail


class AlreadyConfirmError(Exception):
    pass


class FakeConfirmURLError(Exception):
    pass


class RegisterHelper(object):
    """Handle RegisterHelper by interacting with MySQL.
    And sending an confirm email where handle a new RegisterHelper request.
    """

    @staticmethod
    def validate_email(email):
        with get_db_cursor() as cursor:
            SQL = "select 1 from users where email=%s"
            cursor.execute(SQL, (email, ))
            if cursor.fetchone():
                return False
            return True

    @staticmethod
    def validate_name(name):
        with get_db_cursor() as cursor:
            SQL = "select 1 from users where username=%s"
            cursor.execute(SQL, (name, ))
            if cursor.fetchone():
                return False
            return True

    @staticmethod
    def store_to_database(email, name, password):
        salt = os.urandom(32)
        # TODO new in 2.7.8, need more compatibility
        dk = hashlib.pbkdf2_hmac('sha256', bytearray(password),
                                 bytearray(salt), 100000)
        with get_db_cursor() as cursor:
            SQL = "insert users(username, email, password, salt, register_on) \
                   values(%s, %s, %s, %s, NOW());"

            cursor.execute(SQL, (name, email, dk, salt,))

    @staticmethod
    def send_confirm_email(email):
        serializer = ConfirmURLSerializer(config.secret_key_for_confirm_link)
        token = serializer.dumps(email, salt=config.salt_for_confirm_link)
        email_info = config.email_info % token
        send_mail(config.admin_email,
                  config.admin_email_passwd,
                  email,
                  config.email_subject,
                  email_info
                  )

    @staticmethod
    def update_confirmed_label(email):
        with get_db_cursor() as cursor:
            SQL = "update users set confirmed=1 where email=%s"
            cursor.execute(SQL, (email, ))

    @staticmethod
    def confirm_email(token):
        serializer = ConfirmURLSerializer(config.secret_key_for_confirm_link)
        email = serializer.loads(token,
                                 salt=config.salt_for_confirm_link,
                                 max_age=3600)
        if email:
            with get_db_cursor() as cursor:
                SQL = "select confirmed from users where email=%s"
                cursor.execute(SQL, (email, ))
                result = cursor.fetchone()
                if result:
                    confirmed = result[0]
                    if confirmed:
                        raise AlreadyConfirmError()
                    else:
                        RegisterHelper.update_confirmed_label(email)
                        return True
                else:
                    raise FakeConfirmURLError()
        else:
            raise FakeConfirmURLError()
