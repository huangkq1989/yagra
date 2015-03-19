# --*--coding:utf8--*--
"""
    Bussiness Logic for access an avatar by MD5 of user's email.

    For example, when request by an url as follow:
    http://host:port/app.py/avatar/3a201a64275d381416d76205679426d6

    Then will get `3a201a64275d381416d76205679426d6` as a key to query
    the database, and response the corresponding avatar.
"""

import os
import sys

from application.backend.avatar import AvatarHelper
from application.config import config
from application.utility.utility import assemble_avatar_dir
from framework.render_template import print_headers


class VisteAvatar(object):

    def _response_image(self, image_full_name):
        with open(image_full_name, "rb") as fp:
            data = fp.read()
            ext = image_full_name.rsplit('.', 1)[-1]
            # Disable cache.
            headers = {}
            headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            headers["Pragma"] = "no-cache"
            headers["Expires"] = "0"
            print_headers(headers)
            sys.stdout.write("Content-type: image/%s\r\n\r\n" % ext)
            sys.stdout.write(data)

    def visit(self):
        """Get MD5 of avatar from PATH_INFO, then get it's url respone to browser.
        If not exist, return the default avatar to browser.
        """
        avatar_full_name = None
        try:
            request_uri = os.environ['PATH_INFO'][1:]
            result = request_uri.rsplit('/')
            if result:
                key = result[1]
            else:
                key = request_uri
        except KeyError:
            avatar_file = config.default_avatar_file_name
        else:
            avatar_url_in_db = AvatarHelper.select_url_for_avatar(key)
            if avatar_url_in_db:
                avatar_file = avatar_url_in_db
            else:
                avatar_file = config.default_avatar_file_name

        avatar_dir = assemble_avatar_dir()
        avatar_full_name = os.path.join(avatar_dir, avatar_file)
        self._response_image(avatar_full_name)
