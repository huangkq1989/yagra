# --*--coding:utf8--*--
"""
    Utility functions.
"""

import binascii
import os
import smtplib
import struct
import sys
import traceback
from email.mime.text import MIMEText
from email.header import Header
from itertools import izip

from application.config import config
from application.utility import feedback_msg as msg
from framework.render_template import render_template


def constant_time_compare(val1, val2):
    """Returns True if the two strings are equal, False otherwise.
    The time taken is independent of the number of characters that match.  Do
    not use this function for anything else than comparision with known
    length targets.

    >>> constant_time_compare('123', '213')
    False
    >>> constant_time_compare('123', '123')
    True
    >>> constant_time_compare('123', '12')
    False
    >>> constant_time_compare(123, 12)
    Traceback (most recent call last):
    ...
    TypeError: object of type 'int' has no len()
    """
    diff = len(val1) ^ len(val2)
    for x, y in izip(bytearray(val1), bytearray(val2)):
        diff |= x ^ y
    return diff == 0


_trans_5C = b"".join(chr(x ^ 0x5C) for x in range(256))
_trans_36 = b"".join(chr(x ^ 0x36) for x in range(256))


def pbkdf2_hmac(hash_func, password, salt, iterations, dklen=None):
    """Password based key derivation function 2 (PKCS #5 v2.0)
    *Attention*: This function refers to hashlib.py in python2.7.9

    This Python implementations based on the hmac module about as fast
    as OpenSSL's PKCS5_PBKDF2_HMAC for short passwords and much faster
    for long passwords.

    >>> import hashlib
    >>> dk = pbkdf2_hmac(hashlib.sha256, 'password', 'salt', 100000)
    >>> binascii.hexlify(dk)
    '0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5'
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


def send_mail(smtp_server, sender, sender_pw,
              receiver, subject, mail_info, debug=False):
    '''
    >>> from application.utility import confirm_url_serializer
    >>> serializer = confirm_url_serializer.ConfirmURLSerializer()
    >>> email = 'huangkq@foxmail.com'
    >>> token = serializer.dumps(email, salt=config.salt_for_confirm_link)
    >>> email_info = config.email_info.format(
    ...     host='12',
    ...     request_root='122',
    ...     token=token)
    >>> send_mail(config.smtp_server, config.admin_email,
    ...     config.admin_email_passwd, email,
    ...     config.email_subject, email_info, debug=True)
    '''
    msg = MIMEText(mail_info, 'html', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8')
    smtp = smtplib.SMTP()
    smtp.connect(smtp_server)
    smtp.login(sender, sender_pw)
    if debug:
        smtp.set_debuglevel(1)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def cgi_error_logging(message, verbose=True):
    '''Log to http log, for example, when specified directive
    `ErrorLog logs/yagra.com-error_log` in Apache configuration,
    then error info will write to logs/yagra.com-error_log
    '''
    if verbose:
        sys.stderr.write(traceback.format_exc())
    else:
        sys.stderr.write(message)


def render_inform(header, info):
    '''Response inform.html to show notification information.'''
    return render_template(
        'inform.html',
        info_header=header,
        info=info
        )


def render_index(alert_type=msg.SIGNIN_ALERT_TYPE_INFO,
                 info=msg.SIGNIN_MSG_WELCOME):
    '''Response signin.html as index page.'''
    return render_template(
        "signin.html",
        alert_type=alert_type,
        info=info
        )


def get_request_url_for_avatar(avatar_url):
    '''Get request url for avatar with avatar url.
    param: avatar_url: it can be the avatar_url field in db
                       or the default avatar url.
    '''
    return os.path.join(os.environ['REQUEST_ROOT'],
                        config.avatar_dir_name,
                        avatar_url
                        )


def get_default_avatar_request_url():
    '''Get request url for default avatar.'''
    return get_request_url_for_avatar(config.default_avatar_file_name)


def assemble_avatar_dir():
    '''Assemble the avatar dir in filesystem

    Assume that config.avatar_dir_name = 'avatar',
    config.parent_dir_for_avatar_dir = '/tmp'
    then return /tmp/avatar

    Assume that config.avatar_dir_name = 'avatar',
    config.parent_dir_for_avatar_dir = None
    os.environ['DOCUMENT_ROOT'] = '/tmp'
    then return /tmp/avatar
    '''
    if config.parent_dir_for_avatar_dir:
        parent_dir = config.parent_dir_for_avatar_dir
    else:
        parent_dir = os.environ['DOCUMENT_ROOT']
    return os.path.join(parent_dir,
                        config.avatar_dir_name)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
