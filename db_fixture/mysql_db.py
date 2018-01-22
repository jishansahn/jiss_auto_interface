# -*-coding: utf-8-*-
import ConfigParser
import os

import pymysql

from test_suites import common_func

os.chdir(common_func.get_project_dir())


class DB:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read('setup.cfg')
        host = cf.get('db_com', 'host')
        port = int(cf.get('db_com', 'port'))
        user = cf.get('db_com', 'user')
        password = cf.get('db_com', 'password')
        try:
            self.connection = pymysql.connect(host=host,
                                              port=port,
                                              user=user,
                                              password=password,
                                              # db='dbzhb',
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
            self.cur = self.connection.cursor()
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 创建表
    def createDB(self, sqlstr=None):
        if sqlstr != None:
            try:
                self.cur.execute("%s" % (sqlstr))
                # cur.execute("CREATE TABLE IF NOT EXISTS test(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
                self.connection.commit()
            except:
                self.connection.rollback()
            else:
                self.connection.close()
            self.connection.close()

    # 插入数据
    def insertDB(self, sqlstr=None):
        if sqlstr != None:
            try:
                effective_rows=self.cur.execute("%s" % (sqlstr))
                self.connection.commit()
                return effective_rows
            except:
                self.connection.rollback()
        else:
            self.connection.close()
        self.connection.close()

    # 查询数据
    def selectDB(self, sqlstr=None):
        if sqlstr != None:
            try:
                # cur.execute("select * from customer where user_id='2196800' and  user_id='55121'")
                self.cur.execute("%s" % (sqlstr))
                rows = self.cur.fetchall()
                print 'effective rows:', len(rows)
                # print rows[0]
                return rows
                # for row in rows:
                #     # return row
                #     print type(row)
                #     print type(rows)
                #     print "%s" % (row)

            except:
                self.connection.rollback()
            self.connection.close()

    # 删除数据
    def removeDB(self, sqlstr=None):
        if sqlstr != None:
            try:
                effective_rows=self.cur.execute("%s" % (sqlstr))
                self.connection.commit()
                return effective_rows
            except:
                self.connection.rollback()
            self.connection.close()

    # 更新数据
    def updateDB(self, sqlstr=None):
        if sqlstr != None:
            try:
                effective_rows=self.cur.execute("%s" % (sqlstr))
                self.connection.commit()
                print effective_rows
                return effective_rows
            except:
                self.connection.rollback()
            self.connection.close()


if __name__ == "__main__":
    db = DB()
    # db.selectDB('select * from dbzhb.user_car_list where user_id=696549')
    db.updateDB("update dbzhb.user_info set nickname='1006_nicks' where mobile='10000001006' ")
    db.selectDB("select nickname from dbzhb.user_info where mobile='10000001006'")
