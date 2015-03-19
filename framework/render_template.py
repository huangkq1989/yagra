# --*--coding:utf8--*--
"""
    Response view render function.
"""

import os
import re
import cgi


def print_headers(headers):
    '''Print the HTTP header meta.'''
    for k, v in headers.items():
        print '%s: %s' % (k, v)


def redirect(url):
    '''Redirect the request.'''
    print "Status: 302 Moved"
    print "Location: %s" % url
    print


def _get_extends_pattern():
    return re.compile('{%\s*extends\s+(.*?)\s*%}')


def _get_block_pattern():
    return re.compile("""{%\s*block\s+(.*?)\s*%}
                         (.*?)
                         {%\s*endblock\s*%}
                      """, re.MULTILINE | re.VERBOSE | re.DOTALL)


def _form_block_pattern(block_name):
    p = (r"""{%\s*block\s+""" + block_name +
         """\s*%}(.*?){%\s*endblock\s*%}"""
         )
    return re.compile(p, re.MULTILINE | re.DOTALL)


def _get_html_file(file_name):
    return os.path.sep.join([os.environ['DOCUMENT_ROOT'],
                             'static/templates',
                             file_name
                             ])


def render_template(file_name, **kwargs):
    '''Render html to browser, suport extends parent
    template, and support variable.

    Keywords include `extends`, `block`, `endblock`.

    Examples:
        # extends template
        {% extends template.html %}

        # block feature
        {% block blockname %}
        {% endblock %}

        # variable
        {variable}
    '''
    print "Content-type: text/html"
    print
    file_path = _get_html_file(file_name)
    with open(file_path) as fp:
        first_line = fp.readline()
    match = _get_extends_pattern().search(first_line)

    template = None
    if match:
        template_name = match.group(1).strip()
        template_name = _get_html_file(template_name)
        with open(template_name) as fp:
            template = fp.read()

    with open(file_path) as fp:
        data = fp.read()
        for match in _get_block_pattern().finditer(data):
            assert template is not None, "Must have parent template"
            template = re.sub(_form_block_pattern(match.group(1)),
                              match.group(2), template)
        if not template:
            template = data

    if not kwargs:
        kwargs = {}
    kwargs['request_root'] = os.environ['REQUEST_ROOT']
    for k, v in kwargs.iteritems():
        p = re.compile('{\s*' + k + '\s*}')
        escaped_value = cgi.escape(kwargs[k], quote=True)
        template = p.sub(escaped_value, template)

    print template
