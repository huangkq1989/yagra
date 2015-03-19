# --*--coding:utf8--*--
'''
    Configuration for yagra.
'''

import os

# MySQL related.
db_host = "localhost"
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db_name = 'yagra'


# Avatar storage directory and valid type.
avatar_dir_name = 'avatar'
# If it's not `None` it will used as  a parent
# directory for `avatar_dir_name`.
# Else os.environ['DOCUMENT_ROOT'] will used as
# as parent dir for `avatar_dir_name`
parent_dir_for_avatar_dir = None
default_avatar_file_name = 'default.jpg'
valid_extension = tuple('jpg jpe jpeg png gif'.split())

# Confirm link related.
salt_for_confirm_link = '8CD3FC6819F2C2CA0F941D1DAEEA139A'
expired_interval_for_confirm_link = 60 * 60  # Unit is second.


# Configuration for session management.
session_dir_name = 'session'
# Same as parent_dir_for_avatar_dir.
parent_dir_for_session_dir = None
session_expires_interval = 60 * 15  # seconds
session_salt = '0747041A13520271FF3597784650E6BC'


# Log, error will goto error log of apache.
# If this is set to True, then will print traceback,
# else only error message will be logged.
do_verbose_err_log = True


# Configuration for send a confirm email.
smtp_server = 'smtp.163.com'
admin_email = 'yagra_admin@163.com'
admin_email_passwd = 'yagraadmin'
email_subject = 'confirm email from yagra'
email_info = ("<html><body>Welcome, please clink <a href='http://" +
              "{host}{request_root}/app.py/confirm/?url={token}'>" +
              " here </a> to confirm registration.</body></html>"
              )

# Frequency control for using wrong password or username to signin.
threshold = 5
interval_seconds = 5 * 60
forbidden_inerval = 30 * 60
