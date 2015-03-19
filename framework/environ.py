# --*--coding:utf8--*--
"""
    Initial a REQUEST_ROOT environment variable, use it 
    to avoid hardcode request uri in static files.
"""

import os


def init_request_root(entry_file):
    '''Get the root of request uri, avoid hardcode the request path.
       When change the `Alias` in apache, no need to change the
       source code.

       Example: if request is http://ip:port/yagra/app.py, then
                os.environ['REQUEST_ROOT'] set to /yagra

       Other modules rely on it, so *MUST* call it in the entry of app
       before import other modules in the app. Call it like this:

            init_request_root(__file__)
    '''
    assert entry_file != __file__, \
        "entry_file MUST be the entry of your app"
    request_uri = os.environ['REQUEST_URI']
    base_name = os.path.basename(entry_file)
    request_root = request_uri.split(base_name)[0][:-1]
    request_root = request_root if request_root != '/' else ''
    os.environ['REQUEST_ROOT'] = request_root
