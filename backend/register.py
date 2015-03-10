#!/usr/local/bin/python2.7
#!--*--coding:utf8--*--

import hashlib
import binascii
import os

#import mysql_python


class RegisterHelper(object):
    """Handle RegisterHelper by interacting with MySQL.
    And sending an confirm email where handle a new RegisterHelper request.
    """

    @staticmethod
    def validate_email(email):
        #TODO
        return True

    @staticmethod
    def validate_name(name):
        #TODO
        return True

    @staticmethod
    def store_to_database(email, name, password):
        salt = os.urandom(32)
        #hashlib.md5(password+slat)
        #TODO new in 2.7.8
        dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
        #print len(binascii.hexlify(os.urandom(32)))

    @staticmethod
    def send_confirm_email(email):
        #TODO
        pass

    @staticmethod
    def confirm_email(token):
        #TODO
        return True


if __name__=='__main__':
    RegisterHelper.store_to_database('sha256', '', 'password')
