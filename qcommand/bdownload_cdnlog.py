# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import CdnManager, Auth
from util import write_file, to_unicode
from bdownload import Batch_download
from command_threadpool import SimpleThreadPool
from logging import getLogger
from os import mkdir, path, chdir, rename

logger = getLogger("qcommand")

_cdnlog_fileinfo = []


class Bdownload_cdnlog(object):
    def __init__(self, access_key, secret_key, cdn_domain, log_date, save_path,
                 successfile,
                 failurefile, thread_count):
        self.access_key = access_key
        self.secret_key = secret_key
        self.save_path = save_path
        self.cdn_domain = cdn_domain
        self.log_date = log_date
        self.thread_count = thread_count
        self.successfile = successfile
        self.failurefile = failurefile
        self._http_headers = {}

    def url_list(self, domains, ret, info):
        res = False
        try:
            if info.status_code == 200:
                if ret["data"]:
                    log_data = ret["data"]
                    for domain in domains:
                        domain_path = "{0}/{1}".format(self.save_path, domain)
                        if path.exists(domain_path):
                            pass
                        else:
                            mkdir(domain_path)
                        for i in log_data[domain]:
                            log_name = i["name"].split("/")[1]
                            log_url = i["url"]
                            write_file("{0}/{1}.txt".format(domain_path, domain),
                                       "{0},{1}\n".format(log_name, log_url))
                        rename("{0}/{1}.txt".format(domain_path, domain),
                               "{0}/{1}_download.txt".format(domain_path, domain))
                        if "{0}/{1}_download.txt".format(domain_path, domain) in _cdnlog_fileinfo:
                            pass
                        else:
                            _cdnlog_fileinfo.append("{0}/{1}_download.txt".format(domain_path, domain))
                    res = True
                else:
                    return print("No log data")
            elif info.status_code == 401:
                return print("access_key or secret_key error,Login please enter \"qcommand account --help\" for help")
            else:
                return print(info.text_body)
        except Exception as e:
            logger.warn(to_unicode(e))
        finally:
            return res

    def get_cdnlog_url(self):
        if ";" in self.cdn_domain:
            domains = self.cdn_domain.split(";")
        else:
            domains = [self.cdn_domain]
        try:
            auth = Auth(self.access_key, self.secret_key)
            cdn_manager = CdnManager(auth)
            ret, info = cdn_manager.get_log_list_data(domains, self.log_date)
            return self.url_list(domains, ret, info)
        except Exception as e:
            raise e

    def batch_download_cdnlog(self):
        self._inner_threadpool = SimpleThreadPool(self.thread_count)
        try:
            chdir(self.save_path)
            res = self.get_cdnlog_url()
            if res and len(_cdnlog_fileinfo) > 0:
                for cdnlog_file in _cdnlog_fileinfo:
                    if path.exists(path.dirname(cdnlog_file)):
                        pass
                    else:
                        mkdir(path.dirname(cdnlog_file))
                    with open(cdnlog_file, "r") as f:
                        for file_info in f:
                            try:
                                file_info = file_info.rstrip()
                                if len(file_info) > 0:
                                    filename = file_info.split(",")[0]
                                    file_url = file_info.split(",")[1]
                                else:
                                    pass
                                save_path = path.dirname(cdnlog_file)
                                b_download = Batch_download()
                                self._inner_threadpool.add_task(b_download.asycnc_download, file_url, filename,
                                                                save_path, self._http_headers, self.successfile,
                                                                self.failurefile)
                            except Exception as e:
                                logger.warn(to_unicode(e))
                        self._inner_threadpool.wait_completion()
                        result = self._inner_threadpool.get_result()
                        return print(result)
            else:
                return print("No log data")
        except Exception as e:
            logger.warn(to_unicode(e))
            raise e


if __name__ == '__main__':
    access_key = "********"
    secret_key = "********"
    domains = "********"
    date = "********"
    savedir = "./Downloads"
    successfile = "./successfile.txt"
    failurefile = "./failurefile.txt"
    Batch = Bdownload_cdnlog(access_key, secret_key, domains, date, savedir, successfile, failurefile, thread_count=3)
    ret = Batch.batch_download_cdnlog()
    print(ret)
