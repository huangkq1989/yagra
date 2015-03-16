#!--*--coding:utf8--*--

import binascii
import smtplib
import struct
import sys
import traceback
from email.mime.text import MIMEText
from email.header import Header
from itertools import izip

from application.config import config


def constant_time_compare(val1, val2):
    """Returns True if the two strings are equal, False otherwise.
    The time taken is independent of the number of characters that match.  Do
    not use this function for anything else than comparision with known
    length targets.
    """
    diff = len(val1) ^ len(val2)
    for x, y in izip(bytearray(val1), bytearray(val2)):
        diff |= x ^ y
    return diff == 0


_trans_5C = b"".join(chr(x ^ 0x5C) for x in range(256))
_trans_36 = b"".join(chr(x ^ 0x36) for x in range(256))


def pbkdf2_hmac(hash_func, password, salt, iterations, dklen=None):
    """Password based key derivation function 2 (PKCS #5 v2.0)
    -- !!! refer to hashlib.py in python2.7.9

    This Python implementations based on the hmac module about as fast
    as OpenSSL's PKCS5_PBKDF2_HMAC for short passwords and much faster
    for long passwords.
    """

    if not isinstance(password, (bytes, bytearray)):
        password = bytes(buffer(password))
    if not isinstance(salt, (bytes, bytearray)):
        salt = bytes(buffer(salt))

    # Fast inline HMAC implementation
    inner = hash_func()
    outer = hash_func()
    blocksize = getattr(inner, 'block_size', 64)
    if len(password) > blocksize:
        password = hash_func(password).digest()
    password = password + b'\x00' * (blocksize - len(password))
    inner.update(password.translate(_trans_36))
    outer.update(password.translate(_trans_5C))

    def prf(msg, inner=inner, outer=outer):
        # PBKDF2_HMAC uses the password as key. We can re-use the same
        # digest objects and and just update copies to skip initialization.
        icpy = inner.copy()
        ocpy = outer.copy()
        icpy.update(msg)
        ocpy.update(icpy.digest())
        return ocpy.digest()

    if iterations < 1:
        raise ValueError(iterations)
    if dklen is None:
        dklen = outer.digest_size
    if dklen < 1:
        raise ValueError(dklen)

    hex_format_string = "%%0%ix" % (hash_func().digest_size * 2)

    dkey = b''
    loop = 1
    while len(dkey) < dklen:
        prev = prf(salt + struct.pack(b'>I', loop))
        rkey = int(binascii.hexlify(prev), 16)
        for i in xrange(iterations - 1):
            prev = prf(prev)
            rkey ^= int(binascii.hexlify(prev), 16)
        loop += 1
        dkey += binascii.unhexlify(hex_format_string % rkey)

    return dkey[:dklen]


def send_mail(sender, sender_pw, receiver, subject, mail_info, debug=False):
    msg = MIMEText(mail_info, 'html', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect(config.smtp_server)
    smtp.login(sender, sender_pw)
    if debug:
        smtp.set_debuglevel(1)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def cgi_error_logging(message):
    if config.do_verbose_err_log:
        sys.stderr.write(traceback.format_exc())
    else:
        sys.stderr.write(message)
