# -*-coding: utf-8-*-
# @Time: 2017/3/15 13:47
__author__ = 'Mathilda'


class HttpsReq(object):
    def __init__(self, method, url, **kwargs):
        self.method = method
        self.url = url
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class Rsp(object):
    def __init__(self, result=None, error=None, status_code=None):
        self.result = result
        self.error = error
        self.status_code = status_code

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def set_error(self, error):
        self.error = error

    def get_error(self):
        return self.error

    def set_status_code(self, status_code):
        self.status_code = status_code

    def get_status_code(self):
        return self.status_code
