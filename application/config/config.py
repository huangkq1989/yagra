# --*--coding:utf8--*--

import os

db_host = "localhost"
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db_name = 'yagra'

top_request_uri = '/yagra'
index_request_uri = "/".join([top_request_uri, 'app.py', '/'])


avatar_dir_name = 'avatar'
avatar_storage_top_path = os.path.sep.join(
    [os.environ['DOCUMENT_ROOT'],
     avatar_dir_name
     ])
avatar_request_path = os.path.sep.join(
    [top_request_uri, avatar_dir_name])
default_avatar_file_name = 'default.jpg'
default_avatar_url = os.path.sep.join(
    [avatar_request_path, default_avatar_file_name])
VALIDE_EXTENSION = tuple('jpg jpe jpeg png gif'.split())


secret_key_for_confirm_link = 'iADCDdKslJUx'
salt_for_confirm_link = 'SFDKJDicwcir'
expired_interval_for_confirm_link = 60 * 60


smtp_server = 'smtp.163.com'
admin_email = 'yagra_admin@163.com'
admin_email_passwd = 'yagraadmin'
email_subject = 'confirm email from yagra'
email_info = ("<html><body>Welcome, please clink <a href='http://" +
              os.environ['HTTP_HOST'] + top_request_uri +
              "/app.py/confirm/?url=" +
              "%s'>here</a>  to confirm registration.</body></html>"
              )


session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
session_expires_interval = 30  # seconds
session_salt = 'ADFMDsad33dl'


do_verbose_err_log = True
