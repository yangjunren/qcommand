# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth
from requests import get
from os.path import dirname, exists, getsize, isdir, basename
from os import chdir, makedirs, remove, rename
from logging import getLogger
from urllib3 import disable_warnings, exceptions
from urllib.parse import urlparse, quote
from command_threadpool import SimpleThreadPool
from util import to_unicode
from httpx import stream
from tempfile import NamedTemporaryFile
from tqdm import tqdm

logger = getLogger("qcommand")


class Batch_download(object):

    def private_downloadurl(self, access_key, secret_key, cdn_domain, key):
        auth = Auth(access_key, secret_key)
        base_url = "http://{0}/{1}".format(cdn_domain, quote(key, safe="/"))
        private_url = auth.private_download_url(base_url, expires=3600)
        return private_url

    def check_local_filename(self, local_filename):
        local_filename_path = dirname(local_filename)
        # r_path = re.sub(r'\W+', '/', local_filename_path)
        return local_filename_path.lstrip("/")

    def filter_name(self, url):
        file_name = urlparse(url).path[1:]
        return file_name

    def get_totalsize(self, url):
        disable_warnings(exceptions.InsecureRequestWarning)
        rt = get(url, stream=True, verify=False)
        total_size = int(rt.headers['Content-Length'])
        return total_size

    def get_tmpsize(self, tmp_filename):
        if exists(tmp_filename):
            self.size = getsize(tmp_filename)
        else:
            self.size = 0
        return self.size

    def check_finished(self, temp_size, total_size):
        if temp_size == total_size:
            finished = True
        else:
            finished = False
        return finished

    def async_downloadProgress(self, file_url, total_size):
        with NamedTemporaryFile() as download_file:
            with stream("GET", file_url) as response:
                with tqdm(total=total_size, unit_scale=True, unit_divisor=1024, unit="B", desc=file_url) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        download_file.write(chunk)
                        progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

    def async_write_download_file(self, file_url, ret, tmp_filename, total_size, temp_size):
        try:
            self.async_downloadProgress(file_url, total_size)
            with open(tmp_filename, "ab") as f:
                for chunk in ret.iter_raw():
                    if chunk:
                        temp_size += len(chunk)
                        f.write(chunk)
        except Exception as e:
            raise e

    def simple_write_download_file(self, ret, tmp_filename, download_file, progress):
        try:
            num_bytes_downloaded = ret.num_bytes_downloaded
            status_code = ret.status_code
            # response_text = ret.text
            with open(tmp_filename, "ab") as f:
                for chunk in ret.iter_raw():
                    if chunk:
                        download_file.write(chunk)
                        progress.update(ret.num_bytes_downloaded - num_bytes_downloaded)
                        num_bytes_downloaded = ret.num_bytes_downloaded
                        f.write(chunk)
            return status_code
        except Exception as e:
            logger.warn(e)

    def simple_download(self, file_url, filename, save_path, headers, successfile, failurefile):
        if isdir(save_path):
            chdir(save_path)
            if exists(filename):
                pass
            else:
                try:
                    local_filename_path = self.check_local_filename(filename)
                    filename = filename.strip("/")
                    with NamedTemporaryFile() as download_file:
                        with stream("GET", file_url, headers=headers) as f_response:
                            total_size = int(f_response.headers["Content-Length"])
                            with tqdm(total=total_size, unit_scale=True, unit_divisor=1024, unit="B",
                                      desc=file_url) as progress:
                                if f_response.status_code == 200:
                                    if local_filename_path:
                                        if exists(local_filename_path):
                                            status_code = self.simple_write_download_file(f_response, filename,
                                                                                          download_file, progress)
                                        else:
                                            makedirs(local_filename_path, 0o755)
                                            status_code = self.simple_write_download_file(f_response, filename,
                                                                                          download_file, progress)
                                    else:
                                        status_code = self.simple_write_download_file(f_response, filename,
                                                                                      download_file, progress)
                            return status_code, f_response, filename, "{0}/{1}".format(save_path,
                                                                                       local_filename_path), successfile, failurefile
                except Exception as e:
                    logger.warn(e)
                    return print("\nDownload pause.\n")
        else:
            return print("{0} not exists".format(save_path))

    def asycnc_download(self, file_url, filename, save_path, headers, successfile, failurefile):
        if isdir(save_path):
            chdir(save_path)
            if exists(filename):
                pass
            else:
                try:
                    tmp_filename = filename + ".downtmp"
                    temp_size = self.get_tmpsize(tmp_filename)
                    total_size = self.get_totalsize(file_url)
                    local_filename_path = self.check_local_filename(filename)
                    if total_size < temp_size:
                        remove(tmp_filename)
                        headers["Range"] = "bytes=0-"
                    else:
                        headers["Range"] = "bytes={0}-".format(temp_size)
                    with stream('GET', file_url, headers=headers) as f_response:
                        if f_response.status_code == 200 or f_response.status_code == 206:
                            if exists(tmp_filename):
                                self.async_write_download_file(file_url, f_response, tmp_filename, total_size,
                                                               temp_size)
                            else:
                                if local_filename_path:
                                    if exists(local_filename_path):
                                        self.async_write_download_file(file_url, f_response, tmp_filename, total_size,
                                                                       temp_size)
                                    else:
                                        makedirs(local_filename_path, 0o755)
                                        self.async_write_download_file(file_url, f_response, tmp_filename, total_size,
                                                                       temp_size)
                                else:
                                    self.async_write_download_file(file_url, f_response, tmp_filename, total_size,
                                                                   temp_size)
                except Exception as e:
                    return print("\nDownload pause.\n")
                finally:
                    local_filename = basename(self.filter_name(file_url))
                    tmp_filename = local_filename + ".downtmp"
                    temp_size = self.get_tmpsize(tmp_filename)
                    total_size = self.get_totalsize(file_url)
                    finished = self.check_finished(temp_size, total_size)
                    if finished:
                        rename(tmp_filename, local_filename)
                    return finished, f_response, filename, save_path, local_filename, successfile, failurefile
        else:
            return print("{0} not exists".format(save_path))

    def batch_download(self, accesskey, secretkey, domain, inputfile, savedir, http_headers, private,
                       successfile, failurefile, thread_count=3):
        self._inner_threadpool = SimpleThreadPool(thread_count)
        try:
            with open(inputfile, "r") as f:
                for filename in f:
                    if "," in filename:
                        filename = filename.split(",")[0]
                    else:
                        filename = filename.rstrip()
                    if private:
                        file_url = self.private_downloadurl(accesskey, secretkey, domain, filename)
                    else:
                        file_url = "http://{0}/{1}".format(domain, quote(filename, safe="/"))
                    try:
                        self._inner_threadpool.add_task(self.asycnc_download, file_url, filename, savedir,
                                                        http_headers,
                                                        successfile, failurefile)
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
    domain = "qb8z8byyd.bkt.clouddn.com"
    inputfile = "/Users/yjr18809483524/Downloads/qcommand_test/123.txt"
    savedir = "/Users/yjr18809483524/Downloads/qcommand_test"
    private = False
    http_headers = {}
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    Batch = Batch_download()
    Batch.batch_download(accesskey, secretkey, domain, inputfile, savedir, http_headers, private, successfile,
                         failurefile, thread_count=3)
