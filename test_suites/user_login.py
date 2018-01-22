# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/20
# -*-coding: utf-8-*-
import ConfigParser
import json
import os

import requests

import db_fixture.mysql_db
from test_suites import common_func

os.chdir(common_func.get_project_dir())
print os.getcwd()
cf = ConfigParser.ConfigParser()
cf.read('setup.cfg')

web_host = cf.get('web_host', 'web_host')

version = cf.get('params', 'app_version')


# mobile = cf.get('user', 'mobile')
# verify = cf.get('user', 'verify')

def get_cookies(mobile, v_verify):
    login_url = web_host + '/yiiapp/system/user-login'

    s = requests.session()
    requests.packages.urllib3.disable_warnings()
    # get cookie
    # verify_code
    verify_code = get_verifycode(mobile, s, v_verify)
    # use above cookie to login
    user = {'mobile': mobile, 'verify_code': verify_code}
    r2 = s.post(login_url, data=user, verify=False)
    if json.loads(r2.text)['return_code'] == '0':
        print "login success:", r2.cookies
        return r2.cookies
    else:
        print 'login fail'


def get_verifycode(mobile, s, v_verify):
    send_verify_url = web_host + '/yiiapp/system/send-verify-code'
    verify_data = {'version': version, 'mobile': mobile, 'verify': v_verify}
    rsp = s.post(send_verify_url, data=verify_data, verify=False)
    if json.loads(rsp.text)['return_code'] == '0':
        print '\n send verify code success:', rsp.cookies
        select_code = select_verify_code(mobile)
        return select_code


def select_verify_code(mobile):
    db = db_fixture.mysql_db.DB()
    sqlstr = "select * from dbzhb.mobile_verify_code where mobile='" + mobile + "' order by id desc limit 1"
    print sqlstr
    rows = db.selectDB(sqlstr=sqlstr)
    if len(rows) > 0:
        last_verify_code = rows[0].get('last_verify_code')
        print last_verify_code
        return last_verify_code
    else:
        print 'get no verify code'


# https://www.zuihuibao.cn/yiiapp/system/query-login-status
# {
# 	"return_code": "0",
# 	"return_message": "",
# 	"data": {
# 		"login_status": -1,
# 		"login_type": "-1"
# 	}
# }

if __name__ == "__main__":
    get_cookies()
