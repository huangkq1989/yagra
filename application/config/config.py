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


# Request info.
top_request_uri = os.environ['REQUEST_ROOT']
index_request_uri = "/".join([top_request_uri, 'app.py', '/'])


# Avatar storage directory and valid type.
avatar_dir_name = 'avatar'
default_avatar_file_name = 'default.jpg'
valid_extension = tuple('jpg jpe jpeg png gif'.split())
avatar_storage_top_path = os.path.sep.join(
    [os.environ['DOCUMENT_ROOT'],
     avatar_dir_name
     ])
avatar_request_path = os.path.sep.join(
    [top_request_uri, avatar_dir_name]
    )
default_avatar_url = os.path.sep.join(
    [avatar_request_path, default_avatar_file_name]
    )


# Confirm link related.
secret_key_for_confirm_link = '565F7E67B0BC32301FCA230F33EF5E0A'

salt_for_confirm_link = '8CD3FC6819F2C2CA0F941D1DAEEA139A'
expired_interval_for_confirm_link = 60 * 60  # Unit is second.


# Configuration for send a confirm email.
smtp_server = 'smtp.163.com'
admin_email = 'yagra_admin@163.com'
admin_email_passwd = 'yagraadmin'
email_subject = 'confirm email from yagra'
email_info = ("<html><body>Welcome, please clink <a href='http://" +
              os.environ['HTTP_HOST'] + top_request_uri +
              "/app.py/confirm/?url=" +
              "%s'>here </a> to confirm registration.</body></html>"
              )


# Configuration for session management.
session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
session_expires_interval = 60 * 15  # seconds
session_salt = '0747041A13520271FF3597784650E6BC'


# Log.
do_verbose_err_log = True
