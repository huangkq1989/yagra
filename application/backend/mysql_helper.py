#!--*--coding:utf8--*--

import contextlib
import sys

import MySQLdb

from application.config import config


@contextlib.contextmanager
def get_db_cursor():
    connect = MySQLdb.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        passwd=config.db_passwd,
        db=config.db_name,
        )
    try:
        yield connect.cursor()
    except Exception as err:
        (exc, exc_type, tb) = sys.exc_info()
        raise err, None, tb
        connect.rollback()
    else:
        connect.commit()
