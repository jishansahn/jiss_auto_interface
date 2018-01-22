# -*-coding: utf-8-*-
# @Time    : 2017/3/16
# @Author  : Mathilda

import importlib
import json

from objectpath import Tree

from db import MySqlHandler
from spongebob.all_configs import all_api_config, all_db_config

PATH = 'PATH'
VALUE = 'VALUE'
DIFF_TYPE = 'DIFF_TYPE'
COMPARE_RESULT = 'type'
TYPE = 'TYPE'

DEFAULT_PROTOCOL_LIST = ['http']
# DEFAULT_TOKEN_SQL = "select a.access_token from hr_device_user as a inner join hr_user as b on a.user_id = b.id " \
#                     "where a.device_type = {device_type} and a.is_valid = 1 and b.email = '{user_email}'"
DEFAULT_TOKEN_SQL = "select s.session_id from session as s inner join user_info as u on s.user_id = u.user_id " \
                     "where s.login_type = {login_type} and s.has_login = 1 and u.mobile = '{mobile}'"
DEFAULT_DB_NAME = "dbzhb"

WEIXIN_TYPE = 1
MOBILE_TYPE = 2
THIRD_TYPE = 3


def get_tools(api_info):
    tool_list = []

    def get_tool_by_module(module, protocol_type):
        for x in dir(module):
            if (not x.startswith('_')) and get_type(module, x) == protocol_type:
                tool = getattr(module, x)
                return tool

    api_config = all_api_config.get(api_info.get('api_name'))
    api_type = api_config.get('type').lower()
    if api_type not in DEFAULT_PROTOCOL_LIST:
        print 'Only support %s' % DEFAULT_PROTOCOL_LIST
        return
    call_module = importlib.import_module('.call', 'spongebob')
    assemble_module = importlib.import_module('.assemble', 'spongebob')
    call_tool = get_tool_by_module(call_module, api_type)
    assemble_tool = get_tool_by_module(assemble_module, api_type)
    tool_list.append(call_tool)
    tool_list.append(assemble_tool)
    return tool_list


def get_type(module, cls):
    cls_obj = getattr(module, cls)
    if hasattr(cls_obj, '__protocol_type__'):
        return getattr(module, cls).__protocol_type__.lower()


# def get_pool_manager_config(srv_info):
#     pool_config = {
#         'client': 'pycy',
#         'lazy_load': False,
#         'pool': 'base',
#         'services': {}
#     }
#     pool_config['services'].update(
#         {srv_info.get('service'): {'host': srv_info.get('host'), 'port': srv_info.get('port')}})
#     return pool_config


# def get_pool_manager(srv_info):
#     config = get_pool_manager_config(srv_info)
#     try:
#         pool_manager = ClientsPoolManager(tracking='pcd_test', lazy_load=True)
#         pool_manager.read_config(config)
#     except Exception as e:
#         print 'init pool_manager failed, %s' % e
#         return None
#     else:
#         return pool_manager


def check_json(path, respect_value, source_data):
    real_value = get_json_result(source_data, path)
    print "\nAttention!!!START TO CHECK JSON!!!\n"
    print "***************response***************\n"
    print eval("u'''%s'''" % json.dumps(source_data))
    print "\n*****************path*****************\n"
    print eval("u'''%s'''" % json.dumps(path))
    print "\n***result_get_by_path_from_response***\n"
    print eval("u'''%s'''" % json.dumps(real_value))
    print "\n************respect_result************\n"
    print eval("u'''%s'''" % json.dumps(respect_value))

    diff = compare(respect_value, real_value)
    is_check_pass = print_diff_and_return_false(diff) if diff else True
    return is_check_pass


def check_not_json(path, respect_value, source_data):
    real_value = get_object_result(path, source_data)
    is_check_pass = True if real_value == respect_value else False
    if not is_check_pass:
        print "\nAttention!!!START TO CHECK JSON!!!\n"
        print "***************response***************\n"
        print source_data
        print "\n*****************path*****************\n"
        print eval("u'''%s'''" % json.dumps(path))
        print "\n***result_get_by_path_from_response***\n"
        print real_value
        print "\n************respect_result************\n"
        print respect_value
    return is_check_pass


def get_object_result(path, source_data):
    path_node = path.split('.')
    result = source_data
    for x in path_node:
        result = get_node(x, result)
    return result


def get_node(node, source_data):
    """a.node = a.get(node) or a or a.node or a[node]
    :param node: 属性名称、key或下标
    :param source_data: 数据来源
    :return: 从source_data中取出的数据
    """
    if isinstance(source_data, (str, int, float)):
        result = source_data
    elif isinstance(source_data, (tuple, list)):
        result = source_data[int(node)]
    elif isinstance(source_data, dict):
        result = source_data.get(node)
    else:
        result = getattr(source_data, node)
    return result


def ordered(obj):
    """对json进行排序
    :param obj:
    :return:
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def get_json_result(source_obj, exp):
    """从json数据中获取相应结果，如果结果是可迭代对象，则转换为列表
    :param source_obj:
    :param exp:
    :return:
    """
    source_obj_tree = Tree(source_obj)
    search_result = source_obj_tree.execute(exp)
    if hasattr(search_result, 'next') and hasattr(search_result, '__iter__'):
        search_result = list(search_result)
    return search_result


def get_db_handler(db_name):
    """根据指定的db_name，通过db config获取相应的db handler
    :param db_name:
    :return:
    """
    db_config = all_db_config.get(db_name)
    if not db_config or (not isinstance(db_config, str)):
        print '%s has not configured right' % db_name
        return None
    elif db_config.startswith('mysql'):
        db_handler = MySqlHandler()
    else:
        print 'config must startswith mysql'
        return None
    return db_handler


def get_auth_info(mobile, login_type=THIRD_TYPE):
    """根据用户手机号获取token
    :param mobile: 用户手机号
    :return:
    """
    sql = DEFAULT_TOKEN_SQL.format(user_mobile=mobile, login_type=login_type)
    mysql_handler = MySqlHandler()
    result = mysql_handler.call(db_name=DEFAULT_DB_NAME, sql=sql)
    token = result[0].get('session_id')
    return token


def get_default_headers_by_login_type(login_type):
    config = dict()
    if login_type == MOBILE_TYPE:
        config['headers'] = {'DEVICE_TYPE': 'MOBILE', 'VERSION_NAME': '9.9.9', 'VERSION_CODE': 999999}
    else:
        print "only support mobile(2)"
        return None
    return config


# get diff between two json, from svn
class Diff(object):
    def __init__(self, first, second, with_values=False):
        self.difference = []
        self.seen = []
        self.check(first, second, with_values=with_values)

    def check(self, first, second, path='', with_values=False):
        if with_values:
            if not isinstance(first, type(second)):
                self.save_diff((path, type(first).__name__, type(second).__name__), DIFF_TYPE)
                return

        if isinstance(first, dict):
            for key in first:
                # the first part of path must not have trailing dot.
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = "%s.%s" % (path, key)

                if isinstance(second, dict):
                    if second in key:
                        sec = second[key]
                    else:
                        #  there are key in the first, that is not presented in the second
                        self.save_diff((new_path,), PATH)

                        # prevent further values checking.
                        sec = None

                    # recursive call
                    if sec is not None:
                        self.check(first[key], sec, path=new_path, with_values=with_values)
                else:
                    # second is not dict. every key from first goes to the difference
                    self.save_diff((new_path,), PATH)
                    self.check(first[key], second, path=new_path, with_values=with_values)

        # if object is list, loop over it and check.
        elif isinstance(first, list):
            first = sorted(first)
            second = sorted(second)
            for (index, item) in enumerate(first):
                new_path = "%s[%s]" % (path, index)
                # try to get the same index from second
                sec = None
                if second is not None:
                    try:
                        sec = second[index]
                    except (IndexError, KeyError):
                        self.save_diff((new_path, type(item).__name__), PATH)
                        continue

                # recursive call
                self.check(first[index], sec, path=new_path, with_values=with_values)

        # not list, not dict. check for equality (only if with_values is True) and return.
        else:
            if with_values:
                if first != second:
                    self.save_diff((path, first, second), VALUE)
            return

    def save_diff(self, diff_message, type_):
        if diff_message not in self.difference:
            self.seen.append(diff_message)
            self.difference.append((type_, diff_message))


def compare(json1, json2):
    diff1 = Diff(json1, json2, True).difference
    diff2 = Diff(json2, json1, False).difference
    diffs = []
    for date_type, message in diff1:
        new_type = 'CHANGED'
        if date_type == PATH:
            new_type = 'REMOVED'
        elif date_type == DIFF_TYPE:
            new_type = DIFF_TYPE
        diffs.append({'type': new_type, 'message': message})
    for date_type, message in diff2:
        diffs.append({'type': 'ADDED', 'message': message})
    return diffs


def print_diff_and_return_false(diff):
    print "\n************DIFF_BETWEEN_REAL_AND_RESPECT****************\n"
    for x in diff:
        diff_message = x.get('message')
        if x.get(COMPARE_RESULT) == 'ADDED':
            print 'respect_result | path: %s | less\n' % diff_message[0]
        elif x.get(COMPARE_RESULT) == 'REMOVED':
            print 'respect_result | path: %s | more\n' % diff_message[0]
        elif x.get(COMPARE_RESULT) == 'CHANGED':
            print 'respect_result | path: %s | is: %s' % (diff_message[0], diff_message[1])
            print 'real_result | path: %s | is: %s\n' % (diff_message[0], diff_message[2])
        elif x.get(COMPARE_RESULT) == 'DIFF_TYPE':
            print 'respect_result | path: %s | type is: %s' % (diff_message[0], diff_message[1])
            print 'respect_result | path: %s | type is: %s\n' % (diff_message[0], diff_message[2])
    return False

