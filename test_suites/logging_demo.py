# -*-coding: utf-8-*-
# @Author = jishanshan
# @Date = 2018/4/4

import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(module)s  %(lineno)d  %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.debug('often makes a very good meal of %s', 'visiting tourists')
