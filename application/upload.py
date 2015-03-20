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
from application.utility.utility import assemble_avatar_dir
from application.utility.utility import cgi_error_logging
from application.utility.utility import get_request_url_for_avatar
from framework.jsonify import jsonify
from framework.session import Session


class FileTooBigError(Exception):
    pass


class Upload(object):
    CHUNK_SIZE = 1024
    LIMIT_SIZE = CHUNK_SIZE * 10

    def __init__(self):
        """Assume user's id in database is 1,
        uploaded file name is test.jpg,
        config.parent_dir_for_avatar_dir = '/tmp' and
        config.avatar_dir_name = 'avatar', then:

        self._upload_file_name = test.jpg
        self._extension = jpg
        self._safe_file_name = '%010d.%s' % (1, jpg) = 0000000001.jpg
        self._sub_storage_dir = 000/000
        self._full_storage_dir = /tmp/avatar/000/000/
        self._full_avatar_file_name = /tmp/avatar/000/000/0001.jpg
        """
        self._upload_file_name = None
        self._extension = None
        self._safe_file_name = None
        self._sub_storage_dir = None
        self._full_storage_dir = None
        self._full_avatar_file_name = None

    def _validate_file_name(self):
        fn = os.path.basename(self._upload_file_name)
        try:
            self._extension = fn.rsplit('.', 1)[-1].lower()
            if self._extension in config.valid_extension:
                return True
            return False
        except IndexError:
            return False

    def _assemble_full_storage_dir(self, sub_storage_dir):
        parent_dir = assemble_avatar_dir()
        return os.path.join(parent_dir, sub_storage_dir)

    def _prepare_dir_and_filename(self, user_id):
        # Replace the original filename to avoid unsafe symbol
        safe_file_name_str = "%010d.%s" % (user_id, self._extension)
        self._safe_file_name = safe_file_name_str[6:]
        self._sub_storage_dir = os.path.join(safe_file_name_str[0:3],
                                             safe_file_name_str[3:6],
                                             )
        self._full_storage_dir = self._assemble_full_storage_dir(
            self._sub_storage_dir)
        self._full_avatar_file_name = os.path.join(
            self._full_storage_dir,
            self._safe_file_name
            )
        if not os.path.exists(self._full_storage_dir):
            try:
                os.makedirs(self._full_storage_dir, 0770)
            except OSError as err:
                errmsg = ("%s when trying to create the avatar dir:%s." %
                          (err.strerror, self._full_storage_dir)
                          )
                raise OSError(errmsg)

    def _save_file(self):
        # Previous avatar maybe has a another extension. Remove it.
        os.chdir(self._full_storage_dir)
        for f in os.listdir("."):
            if f.startswith(self._safe_file_name[:4]):
                os.remove(f)

        with open(self._full_avatar_file_name, 'wb+') as fp:
            read_size = 0
            while True:
                chunk = self._fileitem.file.read(Upload.CHUNK_SIZE)
                if not chunk:
                    break
                read_size += len(chunk)
                if read_size > Upload.LIMIT_SIZE:
                    raise FileTooBigError()
                else:
                    fp.write(chunk)
        os.chmod(self._full_avatar_file_name, 0660)

    def _assemble_avatar_url_in_db(self):
        return os.path.sep.join([self._sub_storage_dir,
                                 self._safe_file_name
                                 ])

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

            self._prepare_dir_and_filename(user_id)
            self._save_file()

            avatar_url_in_db = self._assemble_avatar_url_in_db()
            AvatarHelper.updata_avatar_key(user_id, avatar_url_in_db)

            avatar_url = get_request_url_for_avatar(avatar_url_in_db)
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
