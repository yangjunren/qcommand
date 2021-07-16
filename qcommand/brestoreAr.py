# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import BucketManager, build_batch_restoreAr, Auth
from logging import getLogger
from itertools import takewhile, repeat
from json import loads
from util import write_file

logger = getLogger("qcommand")


class Batch_restore(object):
    def __init__(self, auth):
        self.auth = auth

    def _iter_count(self, file_name):
        """获取文本行数"""
        buffer = 1024 * 1024
        with open(file_name) as f:
            buf_gen = takewhile(lambda x: x, (f.read(buffer) for _ in repeat(None)))
            return sum(buf.count('\n') for buf in buf_gen)

    def _read_input_file(self, file_name, start, end):
        """读取1000行数据"""
        filename_list = []
        with open(file_name, "r") as f:
            lines = f.readlines()
            for line in lines[start:end]:
                if "," in line:
                    filename = line.split(",")[0]
                else:
                    filename = line.rstrip()
                filename_list.append(filename)
        return filename_list

    def _keys_data(self, file_key, days):
        """格式化文件名和解冻时间"""
        days_value = [days] * len(file_key)
        data = dict(zip(file_key, days_value))
        return data

    def _filter_info(self, info, file_key, restore_results):
        info_list = loads(info.text_body)
        ret_info = self._keys_data(file_key, info_list)
        for key, value in ret_info.items():
            write_file(restore_results, "{0}: {1}\n".format(key, value))

    def _result_info(self, info, file_key, restore_results):
        if info.status_code == 298 and info.text_body:
            self._filter_info(info, file_key, restore_results)
            print("部分或所有请求操作失败，详情见 {0}".format(restore_results))
        elif info.status_code == 200 and info.text_body:
            self._filter_info(info, file_key, restore_results)
            print("操作成功，详情见 {0}".format(restore_results))
        else:
            print(info)

    def batch_restore(self, bucket_name, file_name, days, restore_results):
        try:
            b_restore = BucketManager(self.auth)
            rows_count = self._iter_count(file_name)
            if rows_count <= 1000:
                file_key = self._read_input_file(file_name, 0, rows_count + 1)
                keys = self._keys_data(file_key, days)
                ops = build_batch_restoreAr(bucket_name, keys)
                _, info = b_restore.batch(ops)
                self._result_info(info, file_key, restore_results)
            else:
                cycles = rows_count // 1000
                i = 0
                while i <= cycles:
                    start = i * 1000
                    end = (i + 1) * 1000
                    if end > rows_count:
                        end = rows_count
                    file_key = self._read_input_file(file_name, start, end)
                    keys = self._keys_data(file_key, days)
                    ops = build_batch_restoreAr(bucket_name, keys)
                    _, info = b_restore.batch(ops)
                    self._result_info(info, file_key, restore_results)
                    i += 1
        except Exception as e:
            logger.warn(e)
            raise e


if __name__ == '__main__':
    access_key = ""
    secret_key = ""
    bucket = ""
    freezeAfter_days = 7
    input_file = "./test.txt"
    result_file = "./resfile_{0}.txt".format(bucket)
    auth = Auth(access_key, secret_key)
    brestore = Batch_restore(auth)
    brestore.batch_restore(bucket, input_file, 7, result_file)
