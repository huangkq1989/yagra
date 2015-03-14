#!--*--coding:utf8--*--

import hashlib

from application.backend.mysql_helper import get_db_cursor


class AvatarHelper(object):

    @staticmethod
    def updata_avatar_key(id, avatar_url):
        SQL = "select email from users where id=%s"
        with get_db_cursor() as cursor:
            cursor.execute(SQL, (id, ))
            result = cursor.fetchone()
            if result:
                email = result[0]
                SQL = "update users set avatar_key=%s, \
                        avatar_url=%s where id=%s"
                avatar_key = hashlib.md5(email).hexdigest()
                cursor.execute(SQL, (avatar_key, avatar_url, id))

    @staticmethod
    def select_url_for_avatar(key):
        with get_db_cursor() as cursor:
            SQL = "select avatar_url from users where avatar_key=%s"
            cursor.execute(SQL, (key, ))
            result = cursor.fetchone()
            if result:
                url = result[0]
                return url
            return None
