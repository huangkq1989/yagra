#!--*--coding:utf8--*--

import contextlib

import MySQLdb


@contextlib.contextmanager
def get_db_cursor():
    connect = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='yagra',
        )
    try:
        yield connect.cursor()
    except Exception as err:
        raise err
        connect.rollback()
    else:
        connect.commit()
