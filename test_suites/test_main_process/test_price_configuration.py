# -*-coding: utf-8-*-
# @Author=jishanshan
import requests
from db_fixture import common_main_proc_db, mysql_db
from test_suites import common_func,user_login


class TestPriceConfig:
    def setup_class(self):
        self.cookies = user_login.get_cookies()
        self.user_id = self.cookies.get('user_id')
        print self.cookies
        print self.user_id
        self.url = common_func.get_host() + '/yiiapp/car-ins/price-configuration'
        self.app_version = common_func.get_app_version()

        self.data = {'id': '',
                     'province': '江苏',
                     'city': '南京',
                     'district': '',
                     'frame_no': '',
                     'license_no': '',
                     'version': self.app_version,
                     'immediate_effect': '1'
                     }

    # 普通用户拉取机构
    # 自建团拉取机构
    # 新车 投保当天拉取的机构
    # 机构的验证
    # activities爆点活动
    # auto_selected 目前后端是写在代码里的
    # 返点是否显示的验证  总返点,公司返点
    # 入团引导 涉及到不同用户身份
    # 高人气
    def setup_method(self, test_price_config_ok):
        # car_id = common_main_proc_db.init_car_data(user_id)
        car_info = common_main_proc_db.get_index_carinfo(self.user_id, car_type=2)
        car_id = car_info.get('id')
        print car_id
        self.data['id'] = car_id

    def test_price_config_ok(self):
        rsp = requests.post(self.url, data=self.data, cookies=self.cookies, verify=False)
        assert rsp.status_code == 200
        rsp_dict = rsp.json()
        print rsp_dict
        assert rsp_dict['return_code'] == '0'
        # 验证返回与系统配置一致？
        # 业务政策系统，这里去sql查询验证？

    def teardown_method(self,test_price_config_ok):
        # TODO
        pass


    def setup_method(self, test_newcar_ins_today):
        # 前置条件,设置保险起期当天
        # user_id = self.get_cookies.get('user_id')
        car_info = common_main_proc_db.get_index_carinfo(self.user_id, car_type=1)
        car_id = car_info.get('id')
        # 获取当前时间+2小时，取整
        v_date, v_hour = common_func.get_add_hours(2)
        update_dict = {'ins_start_date': v_date, 'ins_start_hour': v_hour, 'force_start_date': v_date,
                       'force_start_hour': v_hour}

        upt_str = common_main_proc_db.dict_to_update_sqlstr('dbzhb.user_car_list', update_dict)
        upt_str += " where user_id=" + str(self.user_id) + " and id=" + str(car_id)
        print upt_str
        db = mysql_db.DB()
        effec_rows = db.updateDB(upt_str)
        assert effec_rows == 1 #???? 当数据已经一致时 也会返回0
        self.data['id'] = car_id
        self.data['frame_no'] = car_info.get('frame_no')

    # 验证新车投保当天，带出公司不同，目前支持人保，中华，华安（重庆），这些均依赖于基础配置，故，只粗略验证
    def test_newcar_ins_today(self):
        rsp = requests.post(self.url, data=self.data, cookies=self.cookies, verify=False)
        assert rsp.status_code == 200
        rsp_dict = rsp.json()
        print rsp_dict
        assert rsp_dict['return_code'] == '0'
        assert len(rsp_dict['data']['ins_companies']) < 3

    def teardown_method(self,test_newcar_ins_today):
        # 清数据
        pass
# {
#     "return_code": "0",
#     "return_message": "",
#     "data": {
#         "embed": [],
#         "ins_companies": [
#             {
#                 "company": "zhonghua",
#                 "is_open": 1,
#                 "biz_only": 0,
#                 "force_only": 1,
#                 "company_show_refund": "1",
#                 "activities": [],
#                 "auto_select": 1
#             },
#             {
#                 "company": "huaan",
#                 "is_open": 1,
#                 "biz_only": 1,
#                 "force_only": 1,
#                 "company_show_refund": "1",
#                 "activities": [],
#                 "auto_select": 1
#             }
#         ],
#         "show_refund": "1",
#         "in_group": "0",
#         "can_join_group": {
#             "group_id": 1111,
#             "recommender_id": 0,
#             "join_group_title": "加入团队，推广费更高",
#             "join_group_text": "入团享受当地最高推广费，不入团则减3%"
#         },
#         "high_popularity_companies": [
#             {
#                 "company": "renbao",
#                 "biz_only": "0",
#                 "force_only": "0",
#                 "is_open": "1",
#                 "province": "山东",
#                 "city": "烟台",
#                 "district": "",
#                 "show_refund": "1",
#                 "company_show_refund": "1",
#                 "activities": []
#             }
#         ]
#     }
# }
