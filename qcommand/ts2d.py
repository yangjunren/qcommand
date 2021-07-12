# -*- coding: utf-8 -*-
# flake8: noqa
from time import strftime, localtime


def ts2d(timestamp):
    timeArray = localtime(int(str(timestamp)[:10]))
    date = strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return date
