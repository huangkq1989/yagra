#!--*--coding:utf8--*--

import os

import cgitb
cgitb.enable()

top_request_uri = '/yagra'

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

secret_key_for_confirm_link = 'iADCDdKslJUx' 
salt_for_confirm_link = 'SFDKJDicwcir'

admin_email = 'yagra@scn.cn'
admin_email_passwd = 'yagrayagra'
email_subject = 'confirm email from yagra'
email_info = "Welcome, please clink <a href='%s'>here</a> to confirm registration"


session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
session_expires_interval = 30 # seconds
