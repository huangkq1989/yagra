#!--*--coding:utf8--*--

import sys
import smtplib
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
    This is should be implemented in C in order to get it completely right.
    """
    len_eq = len(val1) == len(val2)
    if len_eq:
        result = 0
        left = val1
    else:
        result = 1
        left = val2
    for x, y in izip(bytearray(left), bytearray(val2)):
        result |= x ^ y
    return result == 0


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
