# --*--coding:utf8--*--
"""
    Validate session, if it is ok, check file name's extension
    and file size, then storage it to file system. After that,
    establish mapping of key and uri of avatar.
"""

import cgi
import os
import time

from application.backend.avatar import AvatarHelper
from application.config import config
from application.utility import feedback_msg as msg
from application.utility.json_result import JsonResult
from application.utility.json_result import ErrorJsonResult
from application.utility.utility import cgi_error_logging
from framework.jsonify import jsonify
from framework.session import Session


class FileTooBigError(Exception):
    pass


class Upload(object):
    CHUNK_SIZE = 1024
    LIMIT_SIZE = CHUNK_SIZE * 10

    def __init__(self):
        self._upload_file_name = None
        self._extension = None
        self._safe_file_name = None
        self._sub_storage_dir = None

    def _validate_file_name(self):
        fn = os.path.basename(self._upload_file_name)
        try:
            self._extension = fn.rsplit('.', 1)[-1].lower()
            if self._extension in config.valid_extension:
                return True
            return False
        except IndexError:
            return False

    def _make_storage_dir(self, user_id):
        # Replace the original filename to avoid unsafe symbol
        safe_file_name_str = "%010d.%s" % (user_id, self._extension)
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

    def _read_file(self, path, file_name):
        full_name = path + file_name
        read_size = 0
        with open(full_name, 'wb+') as fp:
            while True:
                chunk = self._fileitem.file.read(Upload.CHUNK_SIZE)
                if not chunk:
                    break
                read_size += len(chunk)
                if read_size > Upload.LIMIT_SIZE:
                    raise FileTooBigError()
                else:
                    fp.write(chunk)

    def _upload_handler(self):
        try:
            sess = Session()
            user_id = sess.data.get('id')
            if ((not user_id) or
                    sess.is_expired(config.session_expires_interval)):
                return jsonify(ErrorJsonResult(msg.INFORM_SESSION_IS_INVALID))
        finally:
            sess.close()

        form = cgi.FieldStorage()
        self._fileitem = form['filename']
        if not self._fileitem.filename:
            return jsonify(ErrorJsonResult(msg.UPLOAD_INVALID_FILE_NAME))

        self._upload_file_name = self._fileitem.filename
        if self._validate_file_name():

            path = self._make_storage_dir(user_id)
            self._read_file(path, self._safe_file_name)

            avatar_url_in_db = os.path.sep.join([self._sub_storage_dir,
                                                 self._safe_file_name
                                                 ])
            AvatarHelper.updata_avatar_key(user_id, avatar_url_in_db)

            avatar_url = os.path.sep.join([config.avatar_request_path,
                                           avatar_url_in_db
                                           ])
            # Append a timestamp to disable browser cached.
            result = {'img': '?'.join([avatar_url, str(time.time())]),
                      'info': msg.UPLOAD_SUCCEED,
                      }
            return jsonify(JsonResult(result))
        else:
            info = msg.UPLOAD_ONLY_SUPPORT % str(config.valid_extension)
            return jsonify(ErrorJsonResult(info))

    def upload(self):
        try:
            self._upload_handler()
        except FileTooBigError:
            return jsonify(ErrorJsonResult(
                msg.UPLOAD_SIZE_TOO_BIG % (Upload.LIMIT_SIZE / 1024))
                )
        except Exception as err:
            cgi_error_logging(err.message,
                              verbose=config.do_verbose_err_log)
            return jsonify(ErrorJsonResult(msg.INFORM_MSG_TRY_IT_AGAIN))


if __name__ == '__main__':
    upload = Upload()
    upload.upload()
