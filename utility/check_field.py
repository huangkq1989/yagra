#!--*--coding:utf8--*--                       

import cgi
import json

from utility.json_result import JsonResult
from utility.json_result import ErrorJsonResult
from utility.jsonify import jsonify


def check_field(field_name):
    def decoder(func):
        def _check_field():
            form = cgi.FieldStorage() 
            field_value = form.getvalue(field_name)
            if field_name not in form:
                return jsonify(ErrorJsonResult("field is missing")) 
            elif func(field_value):
                return jsonify(ErrorJsonResult("field is invalid")) 
            else:
                return jsonify(ErrorJsonResult("it's valid")) 
        return _check_field
    return decoder
