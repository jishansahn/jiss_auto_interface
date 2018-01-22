# -*-coding: utf-8-*-
# @Time    : 2017/4/18
# @Author  : Mathilda
import httplib
import urllib2
import socket
import requests
import json


class HTTPSConnectionV23(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)


class HTTPSHandlerV23(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV23, req)


# install opener
urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV23()))

if __name__ == "__main__":
    params = {'type': 1, 'index': 0, 'limit': 15}
    r = requests.post("https://www.zuihuibao.cn/yiiapp/piazza/article-list",
                      data=params)
    res_dict = json.loads(r.text)
    print res_dict
    assert r.status_code == 200
    assert res_dict['return_code'] == '0'
