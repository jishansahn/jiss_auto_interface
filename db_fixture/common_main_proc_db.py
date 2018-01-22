# -*-coding: utf-8-*-
import mysql_db
import random
import types


# 多字段update语句sql拼接
# update table set field_1='A',field_2='b',field_3='C' where field_4='F'
def dict_to_update_sqlstr(table, v_dict):
    sqlstr = "update " + table + " set "
    i = 0
    v_len = len(v_dict)
    for (key, value) in v_dict.items():
        if type(value) is types.StringType:
            sqlstr += " " + key + "='" + value + "'"
        else:
            sqlstr += " " + key + "=" + str(value)
        i += 1
        if i < v_len:
            sqlstr += ","
    print sqlstr
    return sqlstr


# 多字段insert语句sql拼接
# insert into tableName(col2,col3) values(val2,val3)
def exec_dict_insert(table, v_dict):
    i = 0
    v_len = len(v_dict)
    key_str = "("
    value_str = "("
    for (key, value) in v_dict.items():
        key_str += key
        if type(value) is types.StringType:
            value_str += "'" + value + "'"
        else:
            value_str += str(value)
        i += 1
        if i < v_len:
            key_str += ", "
            value_str += ", "
        else:
            key_str += ")"
            value_str += ")"
    sqlstr = "insert into " + table + key_str + " values" + value_str
    print sqlstr
    db = mysql_db.DB()
    return db.insertDB(sqlstr)

# 获取当前用户下最近第n个更新车辆info
# car_type：0 上牌车，1 未上牌车，2 任意车
def get_index_carinfo(userid, index=0, car_type=2):
    if car_type == 0:
        sqlstr = "select * from dbzhb.user_car_list where user_id='" + userid + "' and license_no!='' order by update_time desc limit " + str(
            index + 1)
    elif car_type == 1:
        sqlstr = "select * from dbzhb.user_car_list where user_id='" + userid + "' and license_no='' order by update_time desc limit " + str(
            index + 1)
    else:
        sqlstr = "select * from dbzhb.user_car_list where user_id='" + userid + "' order by update_time desc limit " + str(
            index + 1)

    print sqlstr
    db = mysql_db.DB()
    rows = db.selectDB(sqlstr)
    if len(rows) > index:
        return rows[index]
    else:
        return 0


# 获取当前用户下随机一车辆id
# car_type：0 上牌车，1 未上牌车，2 任意车
def get_random_carid(userid, car_type=2):
    # TODO
    sqlstr = "select id from dbzhb.user_car_list where user_id='" + userid + "' order by update_time desc "
    print sqlstr
    db = mysql_db.DB()
    rows = db.selectDB(sqlstr)
    max_index = len(rows)
    if max_index > 0:
        random_index = random.randint(0, max_index - 1)
        return rows[random_index].get('id')
    else:
        return 0


if __name__ == "__main__":
    v_dict = {'user_id': 12, 'license_no': '皖D123454', 'frame_no': '13dfefwe'}
    dict_to_insert_sqlstr("dbzhb.user_car_list", v_dict)
    dict_to_update_sqlstr("dbzhb.user_car_list", v_dict)
