# -*-coding: utf-8-*-
# @Time    : 2017/6/30
# @Author  : Mathilda

import pymysql


def do_insert(cursor, db, user_id, from_type, from_signature, from_serial, amount, ordinal, can_donate, active_time, expiration_time):
    sql = "INSERT INTO EMPLOYEE(user_id, from_type, from_serial, from_signature, amount, ordinal, " \
        "can_donate, active_time, expiration_time) VALUES ('%d', '%d', '%s', '%d', '%d', '%d', '%d', '%s', '%s' )" \
        % (user_id, from_type, from_signature, from_serial, amount, ordinal, can_donate, active_time, expiration_time)
    try:
        cursor.execute(sql)
        print '增加一条数据'
        db.commit()
    except Exception:
        db.rollback()


def do_query(cursor, conn):
    sql = "select * from red_packet where user_id = '%d'" % 2195818
    try:
        cursor.execute(sql)
        print '成功查询'
        data = cursor.fetchall()
        # print data
        for i in data:
            print("id:" + str(i[0]) + ' user_id:' + str(i[1]) + ' from_type:' + str(i[2]))
    except Exception:
        print "Error: unable to fecth data"


def do_delete(cursor, db):
    sql = "DELETE FROM red_packet WHERE user_id = '%d'" % 2195818
    try:
        cursor.execute(sql)
        print '已删除'
        db.commit()
    except Exception:
        db.rollback()


def do_update(cursor, db):
    sql = "UPDATE red_packet SET amount = 7500 WHERE user_id = '%d'" % 2195818
    try:
        cursor.execute(sql)
        print '修改成功'
        db.commit()
    except Exception:
        db.rollback()

conn = pymysql.connect(host='localhost', user='wanglijun', password='soinLove_13',
                       database='dbzhb', port=3315, charset='utf8')
cursor = conn.cursor()
do_query(cursor, conn)
do_update(cursor, conn)
do_query(cursor, conn)
# do_delete(cursor, conn)
# do_query(cursor, conn)
do_insert(cursor, conn, '2195818', 16, 4, '1490671874_1', 1500, 3000, 1, '2017-03-01 10:31:14', '2017-08-30 13:30:59')
do_query(cursor, conn)
cursor.close()
conn.close()
