#!/usr/bin/python

import cgi
import cgitb
import os
import hashlib
import time

from config import config
from utility.session import Session
from utility.render_template import render_template
from utility.render_template import render_inform
from backend.avatar import AvatarHelper


cgitb.enable()


class Upload(object):
    VALIDE_EXTENSION = tuple('jpg jpe jpeg png gif'.split())
    
    def __init__(self):
        self._upload_file_name = None
        self._extension = None
        self._safe_file_name = None
        self._sub_storage_dir = None 

    def _validate_file_name(self):
        fn = os.path.basename(self._upload_file_name)
        try:
            self._extension = fn.rsplit('.', 1)[-1].lower()
            if self._extension in Upload.VALIDE_EXTENSION: 
                return True
            return False
        except IndexError as err:
            return False

    def _make_storage_dir(self, id):
        # Replace the original filename to avoid unsafe symbol  
        self._safe_file_name = "%09d.%s" % (id, self._extension)
        self._sub_storage_dir = os.path.sep.join(
                [self._safe_file_name[0:3], 
                 self._safe_file_name[3:6], 
                 ])
        avatar_dir = os.path.sep.join([config.avatar_storage_top_path,
                                       self._sub_storage_dir, ''
                                       ])
        try:
            os.makedirs(avatar_dir)
        except OSError as err:
            pass
        return avatar_dir

    def _upload_handler(self):
        sess = Session(cookie_path='/')
        id = sess.data.get('id')
        if (not id) or sess.is_expired(config.session_expires_interval):
            return render_inform("Upload Failed", info='please login first!')

        form = cgi.FieldStorage()
        fileitem = form['filename']
        if not fileitem.filename:
            return render_inform("Upload Failed", info='invalid file name!')

        self._upload_file_name = fileitem.filename
        if self._validate_file_name():

            path = self._make_storage_dir(id)

            full_name = path + self._safe_file_name
            with open(full_name, 'wb+') as fp:
                fp.write(fileitem.file.read())

            avatar_url_in_db = os.path.sep.join([self._sub_storage_dir, 
                                                 self._safe_file_name
                                                 ])
            AvatarHelper.updata_avatar_key(id, avatar_url_in_db) 

            avatar_url = os.path.sep.join([config.avatar_request_path, 
                                           avatar_url_in_db
                                           ]) 
            return render_template("main.html", 
                                   img=avatar_url+'?'+str(time.time()))
        else:
            ERROR_STR = ("Invalid type of avatar, only %s format support." % 
                         str(Upload.VALIDE_EXTENSION)
                         )
            return render_inform("Upload Failed", ERROR_STR)

    def upload(self):
        self._upload_handler()
        try:
            pass
        except Exception as err:
            render_inform("Wrong Happened", 'Please try it Again')


upload = Upload()
upload.upload()
