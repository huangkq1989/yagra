# --*--coding:utf8--*--
"""
    Router for request.
"""

import cgitb
import functools
import os
import sys

from application.config import config
from application.utility import feedback_msg as msg
from application.utility.utility import cgi_error_logging
from application.utility.utility import render_inform
from application.utility.utility import render_index
from framework.render_template import redirect


class AppRunner(object):
    '''Wraps the cgi app and acts as central object.
    :param: entry_file: file name of the cgi entry. Usually, it
                        should be set to __file__.

    :param: debug: if set to True, then cgitb.enable is on,
                   traceback of error will display in browser.
                   Or, traceback log to HTTP server *ERROR* log,
                   and show user-friendly info to browser.

    '''
    def __init__(self, entry_file, debug=True):

        assert entry_file != __file__, \
            "entry_file MUST be the entry of your app"
        self._entry_file = entry_file
        self._init_request_root(entry_file)
        self._route_map = {}
        self.debug = debug
        if debug:
            cgitb.enable()

    def _init_request_root(self, entry_file):
        '''Get the root of request uri, avoid hardcode the request path.
           When change the `Alias` in apache, no need to change the
           source code.

           Example: if request is http://ip:port/yagra/app.py, then
                    os.environ['REQUEST_ROOT'] set to '/yagra'
           Example: if request is http://ip:port/test/app.py, then
                    os.environ['REQUEST_ROOT'] set to '/test'
           Example: if request is http://ip:port/app.py, then
                    os.environ['REQUEST_ROOT'] set to '' 
        '''
        request_uri = os.environ['REQUEST_URI']
        base_name = os.path.basename(self._entry_file)
        request_root = request_uri.split(base_name)[0][:-1]
        self.request_root = request_root if request_root != '/' else ''
        os.environ['REQUEST_ROOT'] = request_root

    def route(self, *args, **kwargs):
        '''Building the mapping of request and handler

        Example:
            app = AppRunner()
            @app.route('/uri')
            def uri_handler():
                do_something...
        '''
        def wrapped(func):
            self._route_map[args[0]] = func

            @functools.wraps(func)
            def _wrapped():
                pass
            return _wrapped
        return wrapped

    def dispatch_request(self):
        '''Call the handler according to the PATH_INFO'''
        request_uri = None
        try:
            request_uri = os.environ['PATH_INFO']
        except KeyError:
            return render_index()

        try:
            result = request_uri.split('/')
            if len(result) > 2:
                request_uri = '/'+result[1]
            self._route_map[request_uri]()
        except KeyError:
            return render_inform(msg.INFORM_TITLE_ERROR,
                                 msg.INFORM_MSG_PAGE_NOT_FOUND)
        except Exception as err:
            cgi_error_logging(err.message,
                              config.do_verbose_err_log)

            if not self.debug:
                return render_inform(msg.INFORM_TITLE_ERROR,
                                     msg.INFORM_MSG_TRY_IT_AGAIN)
            else:
                # Reraise exception, then cgitb will handle it.
                (exc, exc_type, tb) = sys.exc_info()
                raise err, None, tb
