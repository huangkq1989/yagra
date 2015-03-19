# --*--coding:utf8--*--

'''
    Unify json respon interface.
'''


class JsonResult(object):
    '''Json interface for success request.'''
    code = None
    data = None

    def __init__(self, data, code=400):
        self.code = code
        self.data = data


class ErrorJsonResult(object):
    '''Json interface when a error occurs.'''
    code = None
    descript = None

    def __init__(self, descript, code=500):
        self.code = code
        self.descript = descript


class FormValidateResult(object):
    '''Json respon for bootstrap-fromvalidate.js library.'''
    valid = None

    def __init__(self, valid):
        self.valid = valid
