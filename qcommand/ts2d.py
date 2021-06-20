# -*- coding: utf-8 -*-
# flake8: noqa
import time


def ts2d(timestamp):
    timeArray = time.localtime(int(str(timestamp)[:10]))
    date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return date
