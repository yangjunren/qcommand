# -*- coding: utf-8 -*-

from qiniu import Auth, put_file
import logging, os
from command_threadpool import SimpleThreadPool
from util import to_unicode

logger = logging.getLogger("qcommand")


class Batch_upload(object):
    def __init__(self, access_key, secret_key, file_dir, bucket_name, successfile,
                 failurefile, thread_count):
        self.access_key = access_key
        self.secret_key = secret_key
        self._inner_threadpool = SimpleThreadPool(3)
        self.thread_count = thread_count
        self.file_dir = file_dir
        self.bucket_name = bucket_name
        self.successfile = successfile
        self.failurefile = failurefile

    def get_dir_filename(self, dir):
        local_filenamelist = []
        for dirpath, dirnames, filenames in os.walk(dir, topdown=False):
            for name in filenames:
                local_filenamelist.append(os.path.join(dirpath, name))
        return local_filenamelist

    def _upload(self, localfile, successfile, failurefile):
        try:
            q = Auth(self.access_key, self.secret_key)
            key = localfile.split(self.file_dir)[1][1:]
            token = q.upload_token(self.bucket_name, key, 3600)
            ret, info = put_file(token, key, localfile)
            if ret:
                return localfile, key, info, successfile, failurefile
        except Exception as e:
            logger.warn(to_unicode(e))
            raise e

    def batch_upload(self):
        self._inner_threadpool = SimpleThreadPool(self.thread_count)
        local_filenamelist = self.get_dir_filename(self.file_dir)
        for local_filename in local_filenamelist:
            try:
                self._inner_threadpool.add_task(self._upload, local_filename, self.successfile, self.failurefile)
            except Exception as e:
                logger.warn(to_unicode(e))
        self._inner_threadpool.wait_completion()
        result = self._inner_threadpool.get_result()
        return print(result)


if __name__ == '__main__':
    access_key = "*****"
    secret_key = "*****"
    bucket_name = "*****"
    fildir = "******"
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    Batch = Batch_upload(access_key, secret_key, fildir, bucket_name, successfile, failurefile, thread_count=3)
    ret = Batch.batch_upload()
    print(ret)
