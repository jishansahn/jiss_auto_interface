# -*-coding: utf-8-*-
# __author__ = 'Mathilda'

from util import *

DEFAULT_USER_MOBILE_LENGTH = 11

WEIXIN_TYPE = 1
MOBILE_TYPE = 2
THIRD_TYPE = 3


def call(api_name, args=None, url_params=None, query=None, auth=None, login_type=MOBILE_TYPE):
    """用于向指定接口发送请求，并获取请求结果。调用的api需要已经在config里按照格式配置正确

    返回的为一个封装好的dict，eg：
    {'result': result, 'error': error, 'status_code': status_code}

    result、error有可能是各种类型，如（int、dict、string、list、或者其他的自定义对象）
    status_code: int

    :param api_name: 在api_config里配置的api名称
    :param args: api的请求体参数  (post)
    :param url_params: url里的参数 (带参get)
    :param query: url后的query参数 (get url+参数)
    :param auth: 用户名称或者认证token
    :param login_type: 发送请求的设备类型，weixin(1) ，mobile(2)，第三方登录(3)
    :return:
    """
    api_info = dict()
    api_config = all_api_config.get(api_name)
    if not api_config:
        print "api '%s' has not in config yet" % api_name
        return None

    # mobile端需要默认的headers
    if login_type not in [WEIXIN_TYPE, MOBILE_TYPE, THIRD_TYPE]:
        print 'device type only support weixin(1) mobile(2) third(3)'
        return None
    if login_type in [MOBILE_TYPE]:
        mobile_config = get_default_headers_by_login_type(login_type)
        mobile_config.update(api_config)
        api_config = mobile_config

    # 兼容不传token、直接传token、传手机号这三种情况
    if auth and len(auth) <= DEFAULT_USER_MOBILE_LENGTH:
        try:
            permission_info = get_auth_info(auth, login_type)
            api_info['permission_info'] = permission_info
        except Exception as e:
            print "get auth info failed, %s" % e
            return None
    else:
        api_info['permission_info'] = auth
        api_info['api_name'] = api_name
        api_info['args'] = args
        api_info['url_params'] = url_params
        api_info['query'] = query

    call_tool, assemble_tool = get_tools(api_info)
    req = assemble_tool(api_info=api_info, api_config=api_config).assemble()
    try:
        rsp = call_tool(req=req).call()
    except Exception as e:
        print 'call failed, %s' % e
        return
    if rsp is None:
        print 'rsp is None, you need check the call info'
        return
    rsp_info = dict()
    rsp_info['result'] = rsp.get_result()
    rsp_info['error'] = rsp.get_error()
    rsp_info['status_code'] = rsp.get_status_code()
    return rsp_info


def check(real_result, respect_result):
    """用于检验返回结果是否满足期望

    real_result = {'result': result, 'error': error, 'status_code': stauts_code}
    respect_result = {'exp_1': respect_value_1, 'exp_2': respect_value_2...}

    若要检验result，且result不包含自定义对象，则需要使用object_path的语法
    eg: real_result = {'result': [{'name': 'zhb_a'}, {'name': 'zhb_b'}]}
    若要检验{'name': 'zhb_a'}在列表里，则
    respect_result = {'len($.result[@.name is pcd_a]) is 1': True}

    若result包含自定义对象，则需要使用以&开始的expression
    eg: real_result = {'result': user_order_detail(order_id=1428051096000007...)}
    respect_result = {'&.result.order_id': 1428051096000007}


    :param real_result: 真实的响应对象
    :param respect_result: 期望的结果集合，必须为dict，且格式必须为{'expression': expect_result}
    :return: 返回一个bool类型
    """
    is_check_pass = True
    for path, respect_value in respect_result.iteritems():

        if not is_check_pass:
            break
        # convert string to unicode
        respect_value = json.loads(json.dumps(respect_value))
        if not path.startswith('&.'):
            try:
                is_check_pass = check_json(path=path, respect_value=respect_value, source_data=real_result)
            except Exception as e:
                print 'check failed, %s' % e
                is_check_pass = False
        else:
            real_path = path.split('.', 1)[1]
            try:
                is_check_pass = check_not_json(path=real_path, respect_value=respect_value, source_data=real_result)
            except Exception as e:
                print 'check failed, %s' % e
                is_check_pass = False
    return is_check_pass


def get_result_by_path(path, obj):
    """获取对象指定路径的值，使用两种方式，object_path和[&.a.b.c]
    &.a.b.c用于非json对象
    :param path:
    :param respect_result:
    :return:
    """
    try:
        if path.startswith('&.'):
            real_path = path.split('.', 1)[1]
            result = get_object_result(path=real_path, source_data=obj)
        else:
            result = get_json_result(source_obj=obj, exp=path)
    except Exception as e:
        print 'get result by path failed, %s' % e
        return None
    else:
        return result


def operator_db(db_name, sql):
    """对数据进行增删改查的操作（目前仅支持mysql）

    对mysql增加数据时，会返回增加的行的id；删除、更新只会返回None
    查询会返回包含所查询信息的列表，每个item为一个json对象

    mysql 增:
    result = operator_db(db_name="local", sql="insert into red_packet (`user_id`, `status`) VALUES (2195818, 0)")
    result -> 12345678005
    mysql 删
    result = operator_db(db_name="local", sql="delete from red_packet where `user_id` = 2195818")
    result -> None
    mysql 改
    result = operator_db(db_name="local", sql="update red_packet set status = 5 where user_id = 2195818")
    result -> None
    mysql 查
    result = operator_db(db_name="local", sql="select * from red_packet where user_id = 2195818")
    result -> [{u'user_id': 2195818, u'active_time': u'2017-03-01 10:31:14'},
    {u'user_id': 9835, u'active_time': u'2017-03-01 10:31:14'}]

    :param db_name: config里指定的db_name
    :param sql: 需要执行的sql语句
    :return:
    """
    db_handler = get_db_handler(db_name)
    try:
        result = db_handler.call(db_name, sql)
    except Exception as e:
        print 'Execute db failed, %s, db_name: %s, sql: %s' % (e, db_name, sql)
        return None
    return result


if __name__ == "__main__":
    print operator_db(db_name='dbzhb', sql="select * from red_packet limit 1")
