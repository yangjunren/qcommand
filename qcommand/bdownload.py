# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth
import logging, requests, os, sys
from urllib.parse import urlparse, quote
from command_threadpool import SimpleThreadPool
from util import to_unicode

logger = logging.getLogger("qcommand")


class Batch_download(object):
    def __init__(self, access_key, secret_key, cdn_domain, input_file, save_path, http_headers, private,
                 successfile,
                 failurefile, thread_count):
        self.access_key = access_key
        self.secret_key = secret_key
        self.input_file = input_file
        self.save_path = save_path
        self.cdn_domain = cdn_domain
        self.private = private
        self._http_headers = http_headers
        self.size = 0
        self.thread_count = thread_count
        self.successfile = successfile
        self.failurefile = failurefile

    def private_downloadurl(self, key):
        auth = Auth(self.access_key, self.secret_key)
        base_url = "http://{0}/{1}".format(self.cdn_domain, quote(key, safe="/"))
        private_url = auth.private_download_url(base_url, expires=3600)
        return private_url

    def check_local_filename(self, local_filename):
        local_filename_path = os.path.dirname(local_filename)
        return local_filename_path

    def filter_name(self, url):
        file_name = urlparse(url).path[1:]
        return file_name

    def downloadProgress(self, filename, save_path, local_filename, temp_size, total_size):
        done = int(50 * temp_size / total_size)
        sys.stdout.write("\r%s ====> %s [%s%s] %d%%" % (
            filename, ("{0}/{1}".format(save_path, local_filename)), '█' * done, ' ' * (50 - done),
            100 * temp_size / total_size))
        sys.stdout.flush()

    def get_totalsize(self, url):
        rt = requests.get(url, stream=True, verify=False)
        total_size = int(rt.headers['Content-Length'])
        return total_size

    def get_tmpsize(self, tmp_filename):
        if os.path.exists(tmp_filename):
            self.size = os.path.getsize(tmp_filename)
        else:
            self.size = 0
        return self.size

    def check_finished(self, temp_size, total_size):
        if temp_size == total_size:
            finished = True
        else:
            finished = False
        return finished

    def write_download_file(self, ret, filename, save_path, local_filename, tmp_filename, temp_size, total_size):
        try:
            with open(tmp_filename, "ab") as f:
                for chunk in ret.iter_content(chunk_size=1024):
                    if chunk:
                        temp_size += len(chunk)
                        f.write(chunk)
                        f.flush()
                        self.downloadProgress(filename, save_path, local_filename, temp_size, total_size)
        except Exception as e:
            raise e

    def download(self, file_url, filename, save_path, headers, successfile, failurefile):
        if os.path.isdir(save_path):
            os.chdir(save_path)
            local_filename = self.filter_name(file_url)
            if os.path.exists(local_filename):
                pass
            else:
                try:
                    tmp_filename = local_filename + ".downtmp"
                    temp_size = self.get_tmpsize(tmp_filename)
                    total_size = self.get_totalsize(file_url)
                    local_filename_path = self.check_local_filename(local_filename)
                    headers["Range"] = "bytes={0}-".format(temp_size)
                    with requests.get(file_url, stream=True, headers=headers) as ret:
                        if ret.status_code == 200 or ret.status_code == 206:
                            if os.path.exists(tmp_filename):
                                self.write_download_file(ret, filename, save_path, local_filename, tmp_filename,
                                                         temp_size,
                                                         total_size)
                            else:
                                if local_filename_path:
                                    if os.path.exists(local_filename_path):
                                        self.write_download_file(ret, filename, save_path, local_filename,
                                                                 tmp_filename,
                                                                 temp_size,
                                                                 total_size)
                                    else:
                                        os.makedirs(local_filename_path, 0o755)
                                        self.write_download_file(ret, filename, save_path, local_filename,
                                                                 tmp_filename,
                                                                 temp_size,
                                                                 total_size)
                                else:
                                    self.write_download_file(ret, filename, save_path, local_filename,
                                                             tmp_filename, temp_size,
                                                             total_size)
                        else:
                            ret.close()
                except Exception as e:
                    print(e)
                    print("\nDownload pause.\n")
                finally:
                    local_filename = self.filter_name(file_url)
                    tmp_filename = local_filename + ".downtmp"
                    temp_size = self.get_tmpsize(tmp_filename)
                    total_size = self.get_totalsize(file_url)
                    finished = self.check_finished(temp_size, total_size)
                    if finished:
                        os.rename(tmp_filename, local_filename)
                    return finished, ret, filename, save_path, local_filename, successfile, failurefile
        else:
            return print("{0} not exists".format(save_path))

    def batch_download(self):
        self._inner_threadpool = SimpleThreadPool(self.thread_count)
        try:
            with open(self.input_file, "r") as f:
                for filename in f:
                    if "," in filename:
                        filename = filename.split(",")[0]
                    else:
                        filename = filename.rstrip()
                    if self.private:
                        file_url = self.private_downloadurl(filename)
                    else:
                        file_url = "http://{0}/{1}".format(self.cdn_domain, quote(filename, safe="/"))
                    try:
                        self._inner_threadpool.add_task(self.download, file_url, filename, self.save_path,
                                                        self._http_headers,
                                                        self.successfile, self.failurefile)
                    except Exception as e:
                        logger.warn(to_unicode(e))
                self._inner_threadpool.wait_completion()
                result = self._inner_threadpool.get_result()
                return print(result)
        except Exception as e:
            logger.warn(to_unicode(e))
            raise e


if __name__ == '__main__':
    accesskey = "************"
    secretkey = "************"
    domain = "************"
    inputfile = "************"
    savedir = "************"
    private = False
    http_headers = {}
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    Batch = Batch_download(accesskey, secretkey, domain, inputfile, savedir, http_headers, private,
                           successfile, failurefile, thread_count=3)
    ret = Batch.batch_download()
    print(ret)
