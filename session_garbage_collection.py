# --*--coding:utf8--*--

import os
import logging
import shelve
import sys
import time


class SessionGC(object):
    """Use to remove session file in case of client
    exits session undeservedly. Such as network link outages.
    """

    def __init__(self, session_dir):
        self._run_interval = 6
        self._session_dir = session_dir

    def do_gc(self):
        dir = os.listdir(self._session_dir)
        for file in dir:
            print file
            data = shelve.open(file, writeback=True)
            try:
                expire_time = data['cookie']['expires']
                if expire_time < time.time():
                    os.remove(file)
                    logging.debug("session(%s) was deleted", file)
            except KeyError as err:
                pass

    def do_gc_cron(self):
        try:
            os.chdir(self._session_dir)
            while True:
                logging.debug('start going to check')
                self.do_gc()
                time.sleep(self._run_interval)
        except Exception as err:
            logging.error("Error happens:%s", err)


def init_logging(log_path):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename=log_path,
        filemode='w'
        )


def run_as_daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    os.chdir("/")
    os.setsid()
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    dev_null = '/dev/null'
    si = file(dev_null, 'r')
    so = file(dev_null, 'a+')
    se = file(dev_null, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def usage():
    print 'python %s session_dir log_filename' % __file__
    print 'Example:'
    print '''python session_garbage_collection.py \
/var/www/yagra/session /tmp/yagra_session_gc.log'''
    sys.exit(-1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    run_as_daemonize()
    init_logging(sys.argv[2])
    cleaner = SessionGC(sys.argv[1])
    cleaner.do_gc_cron()
