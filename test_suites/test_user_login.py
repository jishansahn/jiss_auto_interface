import requests
import json
import pytest

url_verify = 'https://www.zuihuibao.cn/yiiapp/system/send-verify-code'
url_login = 'https://www.zuihuibao.cn/yiiapp/system/user-login'

params_verify = {'mobile': '12341234006', 'verify': '314'}
params_login = {'mobile': '12341234006', 'verify_code': '9527'}

#
# def get_verify_code():
#     res = requests.post(url_verify, data=params_verify, verify=False)
#     cookies = res.cookies
#     print cookies
#     res_dict = json.loads(res.text)
#     res_dict['cookies'] = cookies
#     return res_dict
#
#
# def login(cookies):
#     res = requests.post(url_login, data=params_login, cookies=cookies, verify=False)
#     res_dict = json.loads(res.text)
#     return res_dict
#
#
# def test_user_login():
#     result_verify_code = get_verify_code()
#     print result_verify_code
#     assert result_verify_code['return_code'] == '0'
#
#     result_login = login(result_verify_code['cookies'])
#     print result_login
#     assert result_login['return_code'] == '0'


def test_user_login():
    rsp = requests.post(url_verify, params=params_verify, verify=False)
    requests.packages.urllib3.disable_warnings()
    ck = rsp.cookies
    print ck
    result = requests.post(url_login, params=params_login, cookies=ck, verify=False)
    cookies = result.cookies
    return cookies


if __name__ == '__main__':
    pytest.main('-s test_user_login.py')
    # test_user_login()

# cs_url = 'http://ip.taobao.com/service/getIpInfo.php'
# my_param = {'ip': '8.8.8.8'}
#
# r = requests.get(cs_url, params=my_param)
#
# print r.json()['data']['country'].encode('utf-8')
