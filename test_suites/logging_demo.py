# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2018/4/4

import logging
import logging.config

# logging.config.fileConfig('logging.conf')

# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s %(name)-12s %(levelname)-8s %(module)s  %(lineno)d  %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)
# logger.debug('often makes a very good meal of %s', 'visiting tourists')


# logging.basicConfig(filename='logging.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')


class Logcat():
    def __init__(self):
        # 创建一个logger
        self.logger = logging.getLogger("mylogger")
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，将log写入文件中
        fh = logging.FileHandler('logging.log','w')
        fh.setLevel(logging.INFO)
        # 再创建一个handler，将log输出在控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 设置输出格式
        log_format = "%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s"
        formatter = logging.Formatter(log_format)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        #把handler添加到logger里，其实可以理解为汇报给大领导
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # logger.critical(log)
    def info(self,content):
        self.logger.info(content)

    def error(self,content):
        self.logger.error(content)

q = Logcat()
data = "jinsd"
q.info(data)
q.error(data)