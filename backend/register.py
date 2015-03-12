#!/usr/local/bin/python2.7
#!--*--coding:utf8--*--

import hashlib
import binascii
import os

from backend.mysql_helper import get_db_cursor


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
        #TODO new in 2.7.8, need more compatibility
        dk = hashlib.pbkdf2_hmac('sha256', bytearray(password), 
                                 bytearray(salt), 100000)
        with get_db_cursor() as cursor:
            SQL = "insert users(username, email, password, salt, register_on) \
                   values(%s, %s, %s, %s, NOW());"

            cursor.execute(SQL, (name, email, dk, salt,))

    @staticmethod
    def send_confirm_email(email):
        #TODO
        pass

    @staticmethod
    def confirm_email(token):
        #TODO
        return True


if __name__=='__main__':
    RegisterHelper.validate_email('admin@scn.cn')
