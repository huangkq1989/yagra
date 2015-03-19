# --*--coding:utf8--*--
"""
    MySQL operation for signin.
"""

import hashlib
import time

from application.backend import table_name
from application.backend.mysql_helper import get_db_cursor
from application.config import config
from application.utility import feedback_msg as msg
from application.utility.utility import constant_time_compare
from application.utility.utility import pbkdf2_hmac


class ValidUserError(Exception):
    def __init__(self, allowance=-1):
        self.allowance = allowance


class NeedConfirmException(Exception):
    def __init__(self, msg=msg.SIGNIN_NEED_CONFIRM):
        self.message = msg


class TryTooMuchError(Exception):
    def __init__(self, msg=msg.SIGNIN_TRY_TOO_MUCH):
        self.message = msg


class SigninHelper(object):

    THRESHOLD = config.threshold
    INTERVAL_SECONDS = config.interval_seconds 
    FORBIDDEN_INERVAL = config.forbidden_inerval 

    @staticmethod
    def check_valid(name, plain_password):
        '''Check user and password if valid.'''
        allowance = SigninHelper.check_frequency(name)
        SELECT = ("select id, password, salt," +
                  " avatar_url, confirmed  from {0}" +
                  " where username=%s for update"
                  ).format(table_name.USERS)
        user_info = None
        with get_db_cursor() as cursor:
            cursor.execute(SELECT, (name, ))
            user_info = cursor.fetchone()

        if user_info:
            id, password, salt, avatar_url, confirmed = user_info
            dk = pbkdf2_hmac(hashlib.sha256, plain_password, salt, 100000)
            is_valid = constant_time_compare(dk, password)
            if (is_valid and confirmed):
                SigninHelper._reset_freq_meta(name)
                return id, avatar_url
            elif (is_valid and not confirmed):
                SigninHelper._reset_freq_meta(name)
                raise NeedConfirmException()
        raise ValidUserError(allowance)

    @staticmethod
    def check_frequency(name):
        """Check frequency of login, every `INTERVAL_SECONDS` only
        can try `THRESHOLD` at most. If all chance was used up, then
        have to wait for `FORBIDDEN_INERVAL` senconds.
        """

        INSERT = ("insert {0} (username, last_time, allowance) " +
                  " value (%s, %s, %s)").format(table_name.ACCESS_CONTROL)
        SELECT = ("select last_time, allowance " +
                  " from {0} where username=%s for update"
                  ).format(table_name.ACCESS_CONTROL)
        UPDATE = ("update {0}" +
                  " set `last_time`=%s, `allowance`=%s where `username`=%s"
                  ).format(table_name.ACCESS_CONTROL)

        last_time = None
        allowance = None

        with get_db_cursor() as cursor:
            cursor.execute(SELECT, (name,))
            user_info = cursor.fetchone()

            if not user_info:
                allowance = SigninHelper.THRESHOLD - 1
                cursor.execute(INSERT, (name, time.time(), allowance))
                return allowance
            else:
                last_time, allowance = user_info

            if (time.time() - last_time) > SigninHelper.FORBIDDEN_INERVAL:
                allowance = SigninHelper.THRESHOLD - 1
                current = time.time()
                cursor.execute(UPDATE,
                               (current, SigninHelper.THRESHOLD-1, name))
                return allowance
            elif allowance < 1.0:
                raise TryTooMuchError()
            else:
                current = time.time()
                time_passed = current - last_time
                allowance += time_passed * (
                    SigninHelper.THRESHOLD /
                    float(SigninHelper.INTERVAL_SECONDS))
                if (allowance > SigninHelper.THRESHOLD):
                    allowance = SigninHelper.THRESHOLD
                if (allowance < 1.0):
                    raise TryTooMuchError()
                allowance -= 1.0
                cursor.execute(UPDATE, (current, allowance, name))
                return int(allowance)

    @staticmethod
    def _reset_freq_meta(name):
        UPDATE = ("update {0}" +
                  " set `last_time`=%s where `username`=%s"
                  ).format(table_name.ACCESS_CONTROL)
        with get_db_cursor() as cursor:
            cursor.execute(UPDATE, (0, name))
