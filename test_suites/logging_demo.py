# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2018/4/4

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# logger = logging.getLogger()
# handler = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s %(name)-12s %(levelname)-8s %(module)s  %(lineno)d  %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)
# logger.debug('often makes a very good meal of %s', 'visiting tourists')


logging.basicConfig(filename='logging.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
