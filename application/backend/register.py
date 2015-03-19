# --*--coding:utf8--*--
"""
    MySQL operation for registration and confirm email handler.
"""

import hashlib
import os

from application.utility.confirm_url_serializer import AlreadyConfirmError
from application.utility.confirm_url_serializer import FakeConfirmURLError
from application.backend import table_name
from application.backend.mysql_helper import get_db_cursor
from application.config import config
from application.utility.confirm_url_serializer import ConfirmURLSerializer
from application.utility.utility import pbkdf2_hmac
from application.utility.utility import send_mail


class RegisterHelper(object):
    """Handle RegisterHelper by interacting with MySQL.
    And sending an confirm email when handle a new register request.
    """

    @staticmethod
    def validate_email(email):
        with get_db_cursor() as cursor:
            SQL = "select 1 from {0} where email=%s".format(
                table_name.USERS)
            cursor.execute(SQL, (email, ))
            if cursor.fetchone():
                return False
            return True

    @staticmethod
    def validate_name(name):
        with get_db_cursor() as cursor:
            SQL = "select 1 from {0} where username=%s".format(
                table_name.USERS)
            cursor.execute(SQL, (name, ))
            if cursor.fetchone():
                return False
            return True

    @staticmethod
    def store_to_database(email, name, password):
        salt = os.urandom(32)
        dk = pbkdf2_hmac(hashlib.sha256, password, salt, 100000)
        with get_db_cursor() as cursor:
            SQL = "insert {0}(username, email, password, salt, register_on) \
                   values(%s, %s, %s, %s, NOW());".format(table_name.USERS)
            cursor.execute(SQL, (name, email, dk, salt,))

    @staticmethod
    def rollback_record(email):
        """Rollback registration record if something failed
        after insert record.
        """
        with get_db_cursor() as cursor:
            SQL = "delete from {0} where email=%s".format(table_name.USERS)
            cursor.execute(SQL, (email, ))

    @staticmethod
    def send_confirm_email(email):
        serializer = ConfirmURLSerializer()
        token = serializer.dumps(email, salt=config.salt_for_confirm_link)
        email_info = config.email_info.format(
            host=os.environ['HTTP_HOST'],
            request_root=os.environ['REQUEST_ROOT'],
            token=token)
        send_mail(config.smtp_server,
                  config.admin_email,
                  config.admin_email_passwd,
                  email,
                  config.email_subject,
                  email_info
                  )

    @staticmethod
    def update_confirmed_label(email):
        with get_db_cursor() as cursor:
            SQL = "update {0} set confirmed=1 where email=%s".format(
                table_name.USERS)
            cursor.execute(SQL, (email, ))

    @staticmethod
    def check_confirm_link(token):
        serializer = ConfirmURLSerializer()
        email = serializer.loads(
            token,
            salt=config.salt_for_confirm_link,
            max_age=config.expired_interval_for_confirm_link)
        if email:
            with get_db_cursor() as cursor:
                SQL = "select confirmed from {0} where email=%s".format(
                    table_name.USERS)
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
