# -*- coding: utf-8 -*-
# flake8: noqa
from threading import Thread
from logging import getLogger
from six.moves.queue import Queue
from threading import Lock
from time import sleep
from util import write_file
from qiniu import Auth
from qiniu import BucketManager

logger = getLogger("qcommand")


class WorkerThread(Thread):
    def __init__(self, task_queue, *args, **kwargs):
        super(WorkerThread, self).__init__(*args, **kwargs)
        self._task_queue = task_queue
        self._succ_task_num = 0
        self._fail_task_num = 0
        self._ret = list()

    def _bchstatus_bmodtype_args(self, result_args):
        key, ret, successfile, failurefile = result_args
        if ret.status_code == 200:
            self._succ_task_num += 1
            self._ret.append(ret)
            succ_key = "success {0}".format(key)
            write_file(successfile, succ_key)
            return print(succ_key)
        else:
            self._fail_task_num += 1
            fail_key = "failed {0}: {1}".format(key, ret.text_body)
            write_file(failurefile, fail_key)
            return print(fail_key)

    def _bupload_args(self, result_args):
        localfile, key, ret_info, successfile, failurefile = result_args
        if ret_info.status_code == 200:
            self._succ_task_num += 1
            succ_info = "success {0} ----> {1}".format(localfile, key)
            self._ret.append(ret_info)
            write_file(successfile, succ_info)
            return print(succ_info)
        else:
            self._fail_task_num += 1
            fail_info = "failed {0} ----> {1}".format(localfile, key)
            write_file(failurefile, fail_info)
            return print(fail_info)

    def _bdownload_args(self, result_args):
        finished, ret, filename, save_path, local_filename, successfile, failurefile = result_args
        if finished:
            self._succ_task_num += 1
            succ_info = "success {0} ----> {1}/{2}".format(filename, save_path, local_filename)
            self._ret.append(ret.text)
            write_file(successfile, succ_info)
            return print(succ_info)
        else:
            self._fail_task_num += 1
            fail_info = "failed {0} ----> {1} {2}".format(filename, ret.status_code, ret.text)
            write_file(failurefile, fail_info)
            return print(fail_info)

    def _b_m3u8_download_args(self, result_args):
        status_code, response, filename, local_filename_path, successfile, failurefile = result_args
        if status_code == 200:
            self._succ_task_num += 1
            succ_info = "success {0} ----> {1}".format(filename, local_filename_path)
            self._ret.append(response)
            write_file(successfile, succ_info)
            return print(succ_info)
        else:
            self._fail_task_num += 1
            fail_info = "failed {0} ----> {1} {2}".format(filename, status_code, response)
            write_file(failurefile, fail_info)
            return print(fail_info)

    def run(self):
        while True:
            func, args, kwargs = self._task_queue.get()
            if func is None:
                return
            try:
                result_args = func(*args, **kwargs)
                if result_args and len(result_args) == 4:
                    self._bchstatus_bmodtype_args(result_args)
                elif result_args and len(result_args) == 5:
                    self._bupload_args(result_args)
                elif result_args and len(result_args) == 6:
                    self._b_m3u8_download_args(result_args)
                elif result_args and len(result_args) == 7:
                    self._bdownload_args(result_args)

            except Exception as e:
                logger.warn(str(e))
                self._ret.append(e)
            finally:
                self._task_queue.task_done()

    def get_result(self):
        return self._succ_task_num, self._fail_task_num, self._ret


class SimpleThreadPool:

    def __init__(self, num_threads=3):
        self._num_threads = num_threads
        self._queue = Queue(2000)
        self._lock = Lock()
        self._active = False
        self._workers = []
        self._finished = False

    def add_task(self, func, *args, **kwargs):
        if not self._active:
            with self._lock:
                if not self._active:
                    self._workers = []
                    self._active = True
                    for i in range(self._num_threads):
                        w = WorkerThread(self._queue)
                        self._workers.append(w)
                        w.start()

        self._queue.put((func, args, kwargs))

    def release(self):
        while self._queue.empty() is False:
            sleep(5)

    def wait_completion(self):
        self._queue.join()
        self._finished = True
        # 已经结束的任务, 需要将线程都退出, 防止卡死
        for i in range(self._num_threads):
            self._queue.put((None, None, None))

        self._active = False

    def complete(self):
        self._finished = True

    def get_result(self):
        assert self._finished
        detail = [worker.get_result() for worker in self._workers]
        succ_num = sum([tp[0] for tp in detail])
        fail_num = sum([tp[1] for tp in detail])
        return {'success_num': succ_num, 'fail_num': fail_num}


if __name__ == '__main__':

    pool = SimpleThreadPool(2)

    access_key = "*****"
    secret_key = "*****"
    bucket_name = "*****"
    key = "*****"
    storage_type = "0"


    def mod_type(access_key, secret_key, bucket_name, key, storage_type):
        try:
            q = Auth(access_key, secret_key)
            bucket = BucketManager(q)
            # 2表示归档存储，1表示低频存储，0是标准存储
            _, info = bucket.change_type(bucket_name, key, storage_type)
            return info
        except Exception as e:
            logger.warn(e)
            sleep(0.01)


    pool.add_task(mod_type, access_key, secret_key, bucket_name, key, storage_type)

    pool.wait_completion()
    print(pool.get_result())
