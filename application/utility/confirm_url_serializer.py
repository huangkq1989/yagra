# -*- coding: utf-8 -*-
'''
   Confirm url serializer.
'''

import base64
import hashlib
import json
import time

from application.utility import feedback_msg as msg
from application.utility.utility import constant_time_compare


class AlreadyConfirmError(Exception):
    def __init__(self, msg=msg.CONFIRM_URL_CONFIRMED):
        self.message = msg


class FakeConfirmURLError(Exception):
    def __init__(self, msg=msg.CONFIRM_URL_FAKE):
        self.message = msg


class TimedOutURLError(Exception):
    def __init__(self, msg=msg.CONFIRM_URL_TIMEOUT):
        self.message = msg


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

    def __init__(self, secret_key, hash_func=hashlib.sha256):
        self._secret_key = secret_key
        self._sep = '.'
        self._hash_func = hash_func

    def _get_time(self):
        return int(time.time()-EPOCH)

    def _generate_signature(self, value, salt):
        hash_ = self._hash_func(salt + b'yagra' + self._secret_key)
        hash_.update(value)
        sig = hash_.digest()
        return sig

    def dumps(self, obj, salt=None):
        '''Dump email and timestamp as a confirm url.

        return: a confirm url
        '''
        base64_data = base64_encode(json.dumps(obj))

        timestamp = base64_encode(int_to_bytes(self._get_time()))
        value = base64_data + self._sep + timestamp

        sig = self._generate_signature(value, salt)

        return value + self._sep + base64_encode(sig)

    def verify_signature(self, value, sig, salt, max_age):
        '''Recaculate the email and time in the url, compare the result
        with signature in url. Then check  it is timeout or not.
        '''
        try:
            old_sig = base64_decode(sig)
        except Exception:
            raise FakeConfirmURLError()

        sig = self._generate_signature(value, salt)

        result = constant_time_compare(old_sig, sig)
        if result and max_age:
            try:
                target, timestamp = value.rsplit(self._sep, 1)
                timestamp = bytes_to_int(base64_decode(timestamp))
            except Exception:
                raise FakeConfirmURLError()
            else:
                age = self._get_time() - timestamp
                if age > max_age:
                    raise TimedOutURLError()
                return target
        else:
            raise FakeConfirmURLError()

    def loads(self, signed_value, max_age=None, salt=None):
        '''Load the email if the signed_value(url) is valid.

        return: the email which was encoded in the url

        >>> data = seriz.dumps('yagra@gmail.com', 'salt')
        >>> seriz.loads(data, 60, 'salt')
        u'yagra@gmail.com'

        >>> seriz.loads(data+'1', 60, 'salt')
        Traceback (most recent call last):
        ...
        FakeConfirmURLError

        >>> import time
        >>> time.sleep(1)
        >>> seriz.loads(data, 0.1, 'salt')
        Traceback (most recent call last):
        ...
        TimedOutURLError
        '''
        if self._sep not in signed_value:
            raise FakeConfirmURLError()
        value, sig = signed_value.rsplit(self._sep, 1)
        value = self.verify_signature(value, sig, salt, max_age)
        if value:
            value = base64_decode(value)
            return json.loads(value)


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'seriz': ConfirmURLSerializer('key')})
