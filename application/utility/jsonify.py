# --*--coding:utf8--*--

import json


def jsonify(info):
    print "Content-type: application/json"
    print
    print json.JSONEncoder().encode(vars(info))
