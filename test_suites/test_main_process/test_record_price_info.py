# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2017/7/20
from test_suites import user_login,common_func
import requests
import threading

g_cookies=user_login.get_cookies('10000001333',71)
user_id=g_cookies.get('user_id')
g_url=common_func.get_host()+"/yiiapp/car-ins/record-price-info"

class RecordPrice:
    def test_normal_record(self):
        post_time=common_func.get_current_time()
        req_data={
            "car_id":"536222",
            "insurance_company": "",
            "post_time_stamp": post_time,
            "province": "四川",
            "city": "成都",
            "district": "",
            "ins_start_date": "2017-08-10",
            "ins_start_hour": "0",
            "force_start_date": "2017-08-10",
            "force_start_hour": "0",
            "force_only": 0,
            "choose_force": 1,
            "car_broken": 1,
            "non_deduct_car_broken": 1,
            "third_party": 500000,
            "non_deduct_third_party": 1,
            "driver_seat": 10000,
            "non_deduct_driver_seat": 1,
            "passenger_seat": 10000,
            "non_deduct_passenger_seat": 1,
            "car_rob": 1,
            "non_deduct_car_rob": 1,
            "glass_broken": 0,
            "scratch": 0,
            "non_deduct_scratch": 0,
            "car_burn": 0,
            "non_deduct_car_burn": 0,
            "wade_water": 0,
            "non_deduct_wade_water": 0,
            "find_no_third_party": 0,
            "specify_repair_factory": 0,
        }
        ins_list=["RENBAO","TIANAN"]
        # t1=threading.Thread(target=self.single_price,args=("RENBAO",req_data))
        # t2=threading.Thread(target=self.single_price, args=("TIANAN", req_data))
        self.rsp={}
        # t1.start()
        # t2.start()
        self.single_price("TIANAN",req_data)
        print self.rsp["TIANAN"].text

    def single_price(self,ins_name,req_data):
        req_data['insurance_company']=ins_name
        self.rsp[ins_name]=requests.post(g_url,cookies=g_cookies,data=req_data,verify=False)


if __name__=='__main__':
    rp=RecordPrice()
    rp.test_normal_record()