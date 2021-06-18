# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, BucketManager
import time, logging

from command_threadpool import SimpleThreadPool
from util import to_unicode

logger = logging.getLogger("qcommand")


class Batch_delete(object):
    def __init__(self, access_key, secret_key, bucket_name, inputfile, successfile,
                 failurefile, thread_count=3):
        self.access_key = access_key
        self.secret_key = secret_key
        self._inner_threadpool = SimpleThreadPool(3)
        self.thread_count = thread_count
        self.inputfile = inputfile
        self.bucket_name = bucket_name
        self.successfile = successfile
        self.failurefile = failurefile

    def read_inputfile(self, inputfile):
        res = []
        with open(inputfile, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')
                if "," in line:
                    line = line.split(",")[0]
                res.append(line)
        return tuple(res)

    def delete(self, bucket_name, key, successfile, failurefile):
        try:
            q = Auth(self.access_key, self.secret_key)
            bucket = BucketManager(q)
            _, info = bucket.delete(bucket_name, key)
            return key, info, successfile, failurefile
        except Exception as e:
            logger.warn(to_unicode(e))
            time.sleep(0.1)

    def batch_delete(self):
        self._inner_threadpool = SimpleThreadPool(self.thread_count)
        key_list = self.read_inputfile(self.inputfile)
        for key in key_list:
            try:
                self._inner_threadpool.add_task(self.delete, self.bucket_name, key, self.successfile,
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
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    Batch = Batch_delete(access_key, secret_key, bucket_name, inputfile, successfile, failurefile)
    ret = Batch.batch_delete()
    print(ret)
