#!--*--coding:utf8--*--                       

import os 
import re


def print_headers(headers):
    for k, v in headers.items():
        print '%s: %s' % (k, v)


def render_template(file_name, **kwargs):
    print "Content-type: text/html"
    print 
    file_path = os.path.sep.join([os.environ['DOCUMENT_ROOT'],
                                  'static/templates',
                                  file_name
                                  ])
    with open(file_path) as fp:
        data = fp.read()
    if kwargs:
        for k, v in kwargs.iteritems():
            p = re.compile('{'+ k +'}')
            data = p.sub(kwargs[k], data)
    print data


def render_inform(header, info):
    render_template(
            'inform.html',
            info_header=header,
            info=info
            )
