# -*-coding: utf-8-*-
# @Time    : 2017/3/20
# @Author  : Mathilda
import requests
import json
import random
import test_suites.test_user_login
import pytest
# from spongebob.api import check, call, operator_db


def test_article_list():
    ck = test_suites.test_user_login.test_user_login()
    print ck
    url = 'https://www.zuihuibao.cn/yiiapp/piazza/article-list'
    params = {'type': 1, 'index': 0, 'limit': 15}
    rsp = requests.post(url=url, data=params, cookies=ck, verify=False)
    print rsp.text

    # json to python dict
    res_dict = json.loads(rsp.text)
    print type(res_dict)
    # print res_dict

    assert res_dict['return_code'] == '0'
    assert rsp.status_code == 200

    lists = res_dict['data']['article_list']
    assert len(lists) > 0
    lenoflist = len(lists) - 1
    index = random.randint(0, lenoflist)
    item = lists[index]
    assert item['id'] != ''
    assert item['title'] != ''

    # assert check(real_result=rsp, respect_result={'$.status_code': 200})
    # assert check(real_result=rsp, respect_result={'len($.article[@.id is piazza_articles]) is 1': True})
    # article_id = res_dict['data'][0]['id']
    # result_info = operator_db(db_name='dbzhb', sql='select * from pizza_article '
    #                                                'where id = %d and is_effective=1 and pub_status=1' % article_id)
    # real_info = {
    #     'id': result_info[0]['id'],
    #     'title': result_info[0]['title'],
    #     'list_logo': result_info[0]['list_logo'],
    #     'date_time': result_info[0]['date_time'],
    #     'tags': result_info[0][4]['tags'],
    #     'detail_url': result_info[0]['detail_url'],
    #     'view_num': result_info[0]['view_num'],
    #     'video_url': result_info[0]['video_url']
    # }
    # respect_info = {
    #     'id': article_id,
    #     'title': '爆点活动',
    #     'list_logo': 'http://7xpkn8.com2.z0.glb.qiniucdn.com/admin1476166327.png',
    #     'date_time': '02-22',
    #     'tags': '[\"最热\",\"推荐\"]',
    #     'detail_url': 'https://www.zuihuibao.cn/mobile_user/city_point/city_pointnew.html',
    #     'view_num': 2101,
    #     'video_url': ''
    # }
    # assert check(real_result=real_info, respect_result={'$.*': respect_info})

    # s = json.dumps(params)
    # print s
    #
    # s1 = json.loads(s)
    # print s1
    #
    # print s1['type']

if __name__ == '__main__':
    # pytest.main('-s test_article_list.py')
    test_article_list()
