#!--*--coding:utf8--*--

import cgi
import os
import time

from application.config import config
from application.utility.session import Session
from application.utility.render_template import render_template
from application.utility.render_template import render_inform
from application.backend.avatar import AvatarHelper


class Upload(object):

    def __init__(self):
        self._upload_file_name = None
        self._extension = None
        self._safe_file_name = None
        self._sub_storage_dir = None

    def _validate_file_name(self):
        fn = os.path.basename(self._upload_file_name)
        try:
            self._extension = fn.rsplit('.', 1)[-1].lower()
            if self._extension in config.VALIDE_EXTENSION:
                return True
            return False
        except IndexError:
            return False

    def _make_storage_dir(self, id):
        # Replace the original filename to avoid unsafe symbol
        safe_file_name_str = "%09d.%s" % (id, self._extension)
        self._safe_file_name = safe_file_name_str[6:]
        sub_storage_dir = [safe_file_name_str[0:3],
                           safe_file_name_str[3:6],
                           ]
        self._sub_storage_dir = os.path.sep.join(sub_storage_dir)
        avatar_dir = os.path.sep.join([config.avatar_storage_top_path,
                                       self._sub_storage_dir, ''
                                       ])
        if not os.path.exists(config.avatar_storage_top_path):
            os.makedirs(config.avatar_storage_top_path)
        os.chdir(config.avatar_storage_top_path)
        for dir in sub_storage_dir:
            if not os.path.exists(dir):
                os.makedirs(dir)
                os.chdir(dir)
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
            INFO_STR = "Upload success."
            return render_template("main.html",
                                   img=avatar_url+'?'+str(time.time()),
                                   alert_type="info", info=INFO_STR
                                   )
        else:
            ERROR_STR = ("Invalid type of avatar, only %s format support." %
                         str(Upload.VALIDE_EXTENSION)
                         )
            return render_inform("Upload Failed", ERROR_STR)

    def upload(self):
        self._upload_handler()


if __name__ == '__main__':
    upload = Upload()
    upload.upload()
