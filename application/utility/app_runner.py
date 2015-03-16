# --*--coding:utf8--*--

import cgitb
import functools
import os
import sys

from application.config import config
from application.utility.render_template import redirect
from application.utility.render_template import render_inform
from application.utility.utility import cgi_error_logging


class AppRunner(object):
    def __init__(self, debug=True):
        self.route_map = {}
        self.debug = debug
        if debug:
            cgitb.enable()

    def route(self, *args, **kwargs):
        def wrapped(func):
            self.route_map[args[0]] = func

            @functools.wraps(func)
            def _wrapped():
                pass
            return _wrapped
        return wrapped

    def dispatch_request(self):
        request_uri = None
        try:
            request_uri = os.environ['PATH_INFO']
        except KeyError:
            redirect(config.index_request_uri)
            return

        try:
            result = request_uri.split('/')
            if len(result) > 2:
                request_uri = '/'+result[1]
            self.route_map[request_uri]()
        except KeyError:
            return render_inform("Error 404", "Page Not Found")
        except Exception as err:
            cgi_error_logging(err.message)
            if not self.debug:
                return render_inform("Error : (",
                                     "Sorry, please try it again.")
            else:
                # cgitb will handle it.
                (exc, exc_type, tb) = sys.exc_info()
                raise err, None, tb
