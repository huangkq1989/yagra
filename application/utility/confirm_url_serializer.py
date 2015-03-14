# -*- coding: utf-8 -*-

import hmac
import time
import base64
import json
import hashlib

from application.config import config
from application.utility.utility import constant_time_compare


EPOCH = 1293840000


def int_to_bytes(num):
    assert num >= 0
    rv = []
    while num:
        rv.append(chr(num & 0xff))
        num >>= 8
    return b''.join(reversed(rv))


def bytes_to_int(bytestr):
    return reduce(lambda a, b: a << 8 | b, bytearray(bytestr), 0)


def base64_encode(string):
    return base64.urlsafe_b64encode(string).strip(b'=')


def base64_decode(string):
    return base64.urlsafe_b64decode(string + b'=' * (-len(string) % 4))


class ConfirmURLSerializer(object):

    def __init__(self, secret_key):
        self.serializer = json
        self.secret_key = secret_key
        self.sep = '.'

    def want_bytes(s, encoding='utf-8', errors='strict'):
        if isinstance(s, unicode):
            s = s.encode(encoding, errors)
        return s

    def _get_time(self):
        return int(time.time()-EPOCH)

    def _generate_signature(self, value, salt):
        key = hashlib.sha1(salt + b'yagra' + self.secret_key).digest()
        sig = hmac.new(key, msg=value, digestmod=hashlib.sha1).digest()
        return sig

    def dumps(self, obj, salt=None):
        base64_data = base64_encode(json.dumps(obj))

        timestamp = base64_encode(int_to_bytes(self._get_time()))
        value = base64_data + self.sep + timestamp

        sig = self._generate_signature(value, salt)

        return value + self.sep + base64_encode(sig)

    def verify_signature(self, value, sig, salt):
        try:
            old_sig = base64_decode(sig)
        except Exception:
            return False

        sig = self._generate_signature(value, salt)

        result = constant_time_compare(old_sig, sig)
        if result:
            target, timestamp = value.rsplit(self.sep, 1)
            try:
                timestamp = bytes_to_int(base64_decode(timestamp))
            except Exception as e:
                print e
                return False
            else:
                age = self._get_time() - timestamp
                if age > config.expired_interval_for_confirm_link:
                    return False
                return target

    def loads(self, signed_value, max_age=None, salt=None):
        if self.sep not in signed_value:
            return False
        value, sig = signed_value.rsplit(self.sep, 1)
        value = self.verify_signature(value, sig, salt)
        if value:
            value = base64_decode(value)
            return json.loads(value)
