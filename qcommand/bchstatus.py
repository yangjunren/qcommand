# -*- coding: utf-8 -*-
# flake8: noqa
import logging, time
from qiniu import Auth
from qiniu import BucketManager
from command_threadpool import SimpleThreadPool
from util import to_unicode

logger = logging.getLogger("qcommand")


class Batch_chstatus(object):
    def __init__(self, access_key, secret_key, bucket_name, inputfile, sep, successfile,
                 failurefile, thread_count):
        self.access_key = access_key
        self.secret_key = secret_key
        self._inner_threadpool = SimpleThreadPool(3)
        self.thread_count = thread_count
        self.inputfile = inputfile
        self.bucket_name = bucket_name
        self.successfile = successfile
        self.failurefile = failurefile
        self.sep = sep

    def read_inputfile(self, inputfile):
        ret = []
        with open(inputfile, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')
                ret.append(line)
        return tuple(ret)

    def _chstatus(self, bucket_name, key, file_status, successfile, failurefile):
        try:
            q = Auth(self.access_key, self.secret_key)
            bucket = BucketManager(q)
            # 0表示启用，1表示禁用
            _, info = bucket.change_status(bucket_name, key, file_status, cond=None)
            return key, info, successfile, failurefile
        except Exception as e:
            logger.warn(to_unicode(e))
            time.sleep(0.1)

    def batch_chstatus(self):
        self._inner_threadpool = SimpleThreadPool(self.thread_count)
        inputfile_list = self.read_inputfile(self.inputfile)
        for i in inputfile_list:
            try:
                _i = i.split(self.sep)
            except Exception as e:
                logger.warn(to_unicode(e))
                raise e
            _key = _i[0]
            _file_status = _i[1]
            try:
                self._inner_threadpool.add_task(self._chstatus, self.bucket_name, _key, _file_status, self.successfile,
                                                self.failurefile)
            except Exception as e:
                logger.warn(to_unicode(e))
        self._inner_threadpool.wait_completion()
        result = self._inner_threadpool.get_result()
        return print(result)


if __name__ == '__main__':
    access_key = "*****"
    secret_key = "*****"
    bucket_name = "*****"
    inputfile = "******"
    sep = ","
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    thread_count = 3
    Batch = Batch_chstatus(access_key, secret_key, bucket_name, inputfile, sep, successfile, failurefile, thread_count)
    ret = Batch.batch_chstatus()
    print(ret)
