# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, BucketManager
from logging import getLogger

logger = getLogger("qcommand")


def file_restoreAr(access_key, secret_key, bucket, key, freezeAfter_days):
    """节点单个归档文件"""
    try:
        auth = Auth(access_key, secret_key)
        restore = BucketManager(auth)
        _, info = restore.restoreAr(bucket, key, freezeAfter_days)
        if info.status_code == 200:
            print("restore success")
        else:
            print("restore failed {0}".format(info.text_body))
    except Exception as e:
        logger.warn(e)
        return e


if __name__ == '__main__':
    access_key = ""
    secret_key = ""
    bucket = ""
    freezeAfter_days = 7
    input_file = "./test.txt"
    file_restoreAr(access_key, secret_key, bucket, input_file, 7)
