#!--*--coding:utf8--*--

import hashlib
import binascii
import os
import time

#import mysql_python
from backend.mysql_helper import get_db_cursor


class SignInHelper(object):
    """Handle Register by interacting with MySQL.
    And sending an confirm email where handle a new register request.
    """

    @staticmethod
    def check_valid(name, plain_password):
        with get_db_cursor() as cursor:
            SQL = "select id, password, salt, avatar_url, confirmed \
                    from users where username=%s"
            cursor.execute(SQL, (name, ))
            result = cursor.fetchone()
            if result:
                id, password, salt, avatar_url, confirmed = result
                dk = hashlib.pbkdf2_hmac('sha256', bytearray(plain_password), 
                                         bytearray(salt), 100000)
                if dk == password : #TODO and confirmed
                    return True, id, avatar_url
            return False, None, None


if __name__=='__main__':
    pass

