# --*--coding:utf8--*--

import os
import re


def print_headers(headers):
    for k, v in headers.items():
        print '%s: %s' % (k, v)


def redirect(url):
    print "Status: 302 Moved"
    print "Location: %s" % url
    print


def get_extends_pattern():
    return re.compile('{%\s*extends\s+(.*?)\s*%}')


def get_block_pattern():
    return re.compile("""{%\s*block\s+(.*?)\s*%}
                         (.*?)
                         {%\s*endblock\s*%}
                      """, re.MULTILINE | re.VERBOSE | re.DOTALL)


def form_block_pattern(block_name):
    p = (r"""{%\s*block\s+""" + block_name +
         """\s*%}(.*?){%\s*endblock\s*%}""")
    return re.compile(p, re.MULTILINE | re.DOTALL)


def get_html_file(file_name):
    return os.path.sep.join([os.environ['DOCUMENT_ROOT'],
                             'static/templates',
                             file_name
                             ])


def render_template(file_name, **kwargs):
    print "Content-type: text/html"
    print
    file_path = get_html_file(file_name)
    with open(file_path) as fp:
        first_line = fp.readline()
    match = get_extends_pattern().search(first_line)

    template = None
    if match:
        template_name = match.group(1).strip()
        template_name = get_html_file(template_name)
        with open(template_name) as fp:
            template = fp.read()

    with open(file_path) as fp:
        data = fp.read()
        for match in get_block_pattern().finditer(data):
            if template:
                template = re.sub(form_block_pattern(match.group(1)),
                                  match.group(2), template)
            else:
                template = data

    if not kwargs:
        kwargs = {}
    kwargs['request_root'] = os.environ['REQUEST_ROOT']
    for k, v in kwargs.iteritems():
        p = re.compile('{' + k + '}')
        template = p.sub(kwargs[k], template)

    print template


def render_inform(header, info):
    render_template(
        'inform.html',
        info_header=header,
        info=info
        )


def render_index(alert_type="info", info="Welcome"):
    return render_template("signin.html", alert_type=alert_type, info=info)
