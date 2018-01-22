# -*- coding: utf-8 -*-

import json
import copy
from modules import HttpsReq


class AssembleTool(object):
    __protocol_type__ = ''
    __DEFAULT_HEADERS__ = {"Content-Type": "application/json"}
    __DEFAULT_METHOD__ = 'post'
    __config_kw_list__ = []

    def __init__(self, api_info, api_config):
        """
        初始化api_info、api_config_info
        :param api_info:
        :param api_config
        :return:
        """
        if not api_info:
            assert 0, 'api_info is not exist, api_info is %s' % api_info
        if not self._is_config_right(api_config):
            assert 0, 'api config is not right, api_config is %s' % api_config
        self.api_info = api_info
        self.api_config = api_config

    def assemble(self):
        method = self._get_method()
        body = self._get_body()
        url = self._get_url()
        headers = self._get_headers()
        query = self._get_query()
        others = self._get_others()
        req = HttpsReq(method=method, url=url, data=body, headers=headers, params=query, **others)
        return req

    def _get_url(self):
        pass

    def _get_body(self):
        pass

    def _get_method(self):
        method = self.__DEFAULT_METHOD__
        return method

    def _is_config_right(self, config):
        '''
        检验config是否符合规范
        :param config:
        :return:
        '''
        check_result = True
        if not config:
            print 'config is not exist'
            check_result = False
        for kw in self.__config_kw_list__:
            if not config.get(kw):
                check_result = False
                print 'config do not include %s' % kw
        return check_result

    def _get_api_address(self):
        if not self.api_config.get('port'):
            api_address = self.api_config.get('host')
        else:
            api_address = "{host}:{port}".format(host=self.api_config.get('host'), port=self.api_config.get('port'))
        return api_address

    def _get_others(self):
        others = {}
        config_others = self.api_config.get('others')
        if config_others and isinstance(config_others, dict):
            others = config_others
        return others

    def _get_query(self):
        query = {} if not self.api_info.get('query') else self.api_info.get('query')
        return query

    def _get_headers(self):
        headers = copy.deepcopy(self.__DEFAULT_HEADERS__)
        if self.api_config.get('headers'):
            headers.update(self.api_config.get('headers'))
        return headers


class RestfulAssembleTool(AssembleTool):
    __protocol_type__ = 'https'
    __config_kw_list__ = ['type', 'url', 'method']

    def _get_method(self):
        if not self.api_config.get('method'):
            print 'method is not exist'
        method = self.api_config.get('method').lower()
        return method

    def _get_body(self):
        args = {}
        if self.api_info.get('args'):
            args = self.api_info.get('args')
        return json.dumps(args)

    def _get_url(self):
        url = ''
        config_url = self.api_config.get('url')
        if self.api_info.get('url_params'):
            try:
                url = config_url.format(**self.api_info.get('url_params'))
            except KeyError as e:
                print 'url_params should include %s' % e
        else:
            url = config_url
        return url

    def _get_permission_info(self):
        permission_info = self.api_info.get('permission_info')
        return permission_info

    def _get_headers(self):
        headers = super(RestfulAssembleTool, self)._get_headers()
        headers.update({'HTTP_ACCESS_TOKEN': self._get_permission_info(), 'Authorization': self._get_permission_info(),
                        'Cookie': 'HTTP_ACCESS_TOKEN={permission_info}; ZHBSESSID={permission_info};'
                                  .
                       format(permission_info=self._get_permission_info())})
        return headers

    def _get_query(self):
        query = {} if not self.api_info.get('query') else self.api_info.get('query')
        return query

