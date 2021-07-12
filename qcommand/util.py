# -*- coding: utf-8 -*-
# flake8: noqa
from logging import getLogger
from six import binary_type
from time import strptime, mktime

logger = getLogger("qcommand")


def to_unicode(s):
    """将字符串转为unicode"""
    if isinstance(s, binary_type):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError as e:
            raise Exception('your bytes strings can not be decoded in utf8, utf8 support only!')
    return s


def write_file(file_path, ret_info):
    try:
        with open(file_path, "a+") as f:
            f.writelines(ret_info + "\n")
    except Exception as e:
        logger.warn(to_unicode(e))
        raise e


def date2timestamp(date):
    timeArray = strptime(date, "%Y-%m-%d")
    timeStamp = int(mktime(timeArray))
    return timeStamp
