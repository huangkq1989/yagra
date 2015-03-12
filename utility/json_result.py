#!--*--coding:utf8--*--                       


class JsonResult(object):
    code = None
    data = None

    def __init__(self, data, code=400):
        self.code = code
        self.data = data


class ErrorJsonResult(object):
    code = None
    descript = None

    def __init__(self, descript, code=500):
        self.code = code
        self.descript = descript


class FormValidateResult(object):
    valid = None

    def __init__(self, valid):
        self.valid = valid

