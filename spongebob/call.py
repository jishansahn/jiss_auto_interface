# -*- coding: utf-8 -*-

from modules import Rsp
from requests import request


class ResultToRsp(object):
    def __init__(self):
        self.rsp = Rsp()

    def _set_status_code(self, response):
        self.rsp.set_status_code(response.status_code)

    def _set_result(self, response):
        pass

    def _set_error(self, response):
        pass

    def convert(self, response):
        self._set_status_code(response)
        self._set_result(response)
        self._set_error(response)
        return self.rsp


class HTTPResultToRsp(ResultToRsp):
    def _set_result(self, response):
        if response.status_code != 200:
            self.rsp.set_result(result=None)
            return
        elif not response.text:
            self.rsp.set_result(result=None)
            return
        else:
            self.rsp.set_result(result=response.json())
            return

    def _set_error(self, response):
        if response.status_code == 200:
            self.rsp.set_error(error=None)
            return
        elif not response.text:
            self.rsp.set_error(error=None)
            return
        else:
            try:
                self.rsp.set_error(error=response.json())
            except Exception as e:
                print e
                self.rsp.set_error(error='503')
            return


class CallHandler(object):
    __protocol_type__ = ''
    __convert_handler__ = ResultToRsp

    def __init__(self, req):
        self.convert_handler = self.__convert_handler__()
        self.req = req

    def call(self):
        print '\nAttention!!!START TO REQUEST!!!\n'
        try:
            response = request(**self.req.__dict__)
        except Exception as e:
            print e
        print 'request url is: ', response.url
        print 'request headers is: ', response.request.headers
        print 'request body is: ', response.request.body
        print 'request method is: ', response.request.method
        rsp = self.convert_handler.convert(response=response)
        print 'request response is: ', rsp.__dict__
        return rsp


class HttpCallHandler(CallHandler):
    __protocol_type__ = 'http'
    __convert_handler__ = HTTPResultToRsp
