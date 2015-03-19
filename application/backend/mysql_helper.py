# --*--coding:utf8--*--
"""
    
    MySQLdb wrapper, auto handle connection release.
"""

import contextlib
import sys

import MySQLdb

from application.config import config


@contextlib.contextmanager
def get_db_cursor():
    '''Wrapper of getting a cursor of MySQLdb.'''
    connect = MySQLdb.connect(
        host=config.db_host,
        port=config.db_port,
        user=config.db_user,
        passwd=config.db_passwd,
        db=config.db_name,
        )
    try:
        cursor = connect.cursor()
        yield cursor
    except Exception as err:
        connect.rollback()
        (exc, exc_type, tb) = sys.exc_info()
        raise err, None, tb
    else:
        connect.commit()
    finally:
        cursor.close()
        connect.close()
