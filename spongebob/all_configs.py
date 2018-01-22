# -*-coding: utf-8-*-
# @Time: 2017/3/15 13:47
__author__ = 'Mathilda'

ENV = 'test'
# 接口的一些不会变动的配置项
#
# restful类型的api必须指明type为http，需包含接口对应的url（不要包含?后的query参数），method为该接口请求的方式（post、get、put、delete）
# url若包含参数，需要用{}，并指明参数名称
# eg: 'delete_unit': {'type': 'http', 'url': 'https://www.zuihuibao.cn/yiiapp/piazza/article-list',
# 'method': 'post'}

all_api_test_config = {
    # 发送验证码
    'send_verify_code': {'type': 'https', 'method': 'post',
                         'url': 'https://www.zuihuibao.cn/yiiapp/system/send-verify-code'},
    # 获取广场文章列表
    'get_articles_list': {'type': 'https', 'method': 'post',
                          'url': ':https://www.zuihuibao.cn/yiiapp/piazza/article-list'},
    # 登录
    'user_login': {'type': 'https', 'method': 'post',
                   'url': 'https://www.zuihuibao.cn/yiiapp/system/user-login'}
}
all_api_prod_config = {}

all_db_prod_config = {}

# mysql config eg:
# db_name: "mysql://username:password@host:port/db"
all_db_test_config = {
    "local": "mysql://wanglijun:soinLove_13@127.0.0.1:65531/test"
    # "dbzhb": "mysql://dbzhb:rm-bp10nv14m42j808s2.mysql.rds.aliyuncs.com@121.40.53.236:3306/dbzhb"
}

# test service
service_test = {'dbzhb': {'host': '127.0.0.1', 'port': 65531}}
service_prod = {'dbzhb': {'host': 'rr-bp1512gy10ic3x80v.mysql.rds.aliyuncs.com', 'port': 3306}}

if ENV == 'prod':  # 121.41.114.141
    all_api_config = all_api_prod_config
    all_db_config = all_db_prod_config
    all_service_config = service_prod
elif ENV == 'test':  # 121.40.53.236
    all_api_config = all_api_test_config
    all_db_config = all_db_test_config
    all_service_config = service_test
else:
    all_api_config = all_db_config = all_service_config = dict()
