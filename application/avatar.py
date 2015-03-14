# --*--coding:utf8--*--

import os
import sys

from application.backend.avatar import AvatarHelper
from application.config import config


class VisteAvatar(object):

    def _response_image(self, image_full_name):
        with open(image_full_name, "rb") as fp:
            data = fp.read()
            ext = image_full_name.rsplit('.', 1)[-1]
            sys.stdout.write("Content-type: image/%s\r\n\r\n" % ext)
            sys.stdout.write(data)

    def visit(self):
        avatar_full_name = None
        default_avatar = os.path.sep.join([config.avatar_storage_top_path,
                                           config.default_avatar_file_name
                                           ])
        try:
            request_uri = os.environ['PATH_INFO'][1:]
            result = request_uri.rsplit('/')
            if result:
                key = result[1]
            else:
                key = request_uri
        except KeyError:
            avatar_full_name = default_avatar
        else:
            avatar_url_in_db = AvatarHelper.select_url_for_avatar(key)
            if avatar_url_in_db:
                avatar_full_name = os.path.sep.join(
                    [config.avatar_storage_top_path,
                     avatar_url_in_db
                     ])
            else:
                avatar_full_name = default_avatar
        self._response_image(avatar_full_name)


if __name__ == '__main__':
    avatar = VisteAvatar()
    avatar.visit()
