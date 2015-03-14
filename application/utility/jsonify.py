# --*--coding:utf8--*--

import json


class FormValidateResult(object):
    valid = None

    def __init__(self, valid):
        self.valid = valid


def jsonify(info):
    print "Content-type: application/json"
    print
    print json.JSONEncoder().encode(vars(info))
