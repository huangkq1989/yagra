#!/usr/bin/python

import os
import cgi
import cgitb 
import os
import sys

from backend.avatar import AvatarHelper
from config import config

cgitb.enable()


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
            key = os.environ['PATH_INFO'][1:]
        except KeyError as err: 
            avatar_full_name = default_avatar
        else:
            avatar_url_in_db = AvatarHelper.select_url_for_avatar(key)
            if avatar_url_in_db:
                avatar_full_name = os.path.sep.join([config.avatar_storage_top_path,
                                                     avatar_url_in_db
                                                     ])
            else:
                avatar_full_name = default_avatar 
        self._response_image(avatar_full_name)


avatar = VisteAvatar()
avatar.visit()
