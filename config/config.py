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
