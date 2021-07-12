# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import http, config, QiniuMacAuth
import time


class bucket_Btatistic(object):
    def __init__(self, auth):
        self.auth = auth

    def timestamp2date(self, timeStamp):
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def space_ret_info(self, ret, info):
        if ret and info.status_code == 200:
            time_key = ret["times"]
            data_value = ret["datas"]
            data = dict(zip(time_key, data_value))
            for key, value in data.items():
                print("{0}: {1} GB".format(self.timestamp2date(key), (value / 1024 / 1024 / 1024)))
        else:
            print(info)

    def count_ret_info(self, ret, info):
        if ret and info.status_code == 200:
            time_key = ret["times"]
            data_value = ret["datas"]
            data = dict(zip(time_key, data_value))
            for key, value in data.items():
                print("{0}: {1} 个文件".format(self.timestamp2date(key), value))
        else:
            print(info)

    def blob_put_ret_info(self, ret, info, select):
        if ret and info.status_code == 200:
            for i in ret:
                time_key = i["time"]
                size_value = i["values"][select]
                print("{0}: {1} GB".format(time_key, (size_value / 1024 / 1024 / 1024)))
        else:
            print(info)

    def blob_put_count_ret_info(self, ret, info, select):
        if ret and info.status_code == 200:
            for i in ret:
                time_key = i["time"]
                size_value = i["values"][select]
                print("{0}: {1} 次".format(time_key, size_value))
        else:
            print(info)

    def bucket_space(self, begin, end, g, bucket=None, region=None):
        """
        获取标准存储的存储量统计
        https://developer.qiniu.com/kodo/3908/statistic-space
        """
        url = "{0}/v6/space".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region)
        ret, info = self.__get(url, options)
        self.space_ret_info(ret, info)

    def bucket_count(self, begin, end, g, bucket=None, region=None):
        """
        获取标准存储的文件数量统计
        https://developer.qiniu.com/kodo/3914/count
        """
        url = "{0}/v6/count".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region)
        ret, info = self.__get(url, options)
        self.count_ret_info(ret, info)

    def bucket_space_line(self, begin, end, g, bucket=None, region=None, no_predel=False, only_predel=False):
        """
        获取低频存储的存储量统计
        https://developer.qiniu.com/kodo/3910/space-line
        """
        url = "{0}/v6/space_line".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region, no_predel=no_predel,
                                     only_predel=only_predel)
        ret, info = self.__get(url, options)
        self.space_ret_info(ret, info)

    def bucket_count_line(self, begin, end, g, bucket=None, region=None):
        """
        获取低频存储的文件数量统计
        https://developer.qiniu.com/kodo/3915/count-line
        """
        url = "{0}/v6/count_line".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region)
        ret, info = self.__get(url, options)
        self.count_ret_info(ret, info)

    def bucket_space_archive(self, begin, end, g, bucket=None, region=None, no_predel=False, only_predel=False):
        """
        获取归档存储的存储量统计
        https://developer.qiniu.com/kodo/6462/space-archive
        """
        url = "{0}/v6/space_archive".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region, no_predel=no_predel,
                                     only_predel=only_predel)
        ret, info = self.__get(url, options)
        self.space_ret_info(ret, info)

    def bucket_count_archive(self, begin, end, g, bucket=None, region=None):
        """
        获取归档存储的文件数量统计
        https://developer.qiniu.com/kodo/6463/count-archive
        """
        url = "{0}/v6/count_archive".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, bucket=bucket, region=region)
        ret, info = self.__get(url, options)
        self.count_ret_info(ret, info)

    def blob_transfer(self, begin, end, g, select="size", is_oversea=None, taskid=None):
        """
        获取跨区域同步流量统计数据。可查询当天计量，监控统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3911/blob-transfer
        """
        url = "{0}/v6/blob_transfer".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, is_oversea=is_oversea, taskid=taskid)
        ret, info = self.__get(url, options)
        self.blob_put_ret_info(ret, info, select)

    def rs_chtype(self, begin, end, g, select="hits", new_bucket=None, new_region=None):
        """
        获取存储类型转换请求次数。可查询当天计量，监控统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3913/rs-chtype
        """
        url = "{0}/v6/rs_chtype".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, new_bucket=new_bucket, new_region=new_region)
        ret, info = self.__get(url, options)
        self.blob_put_count_ret_info(ret, info, select)

    def internet_traffic_blob_io(self, begin, end, g, select="flow", src="origin", new_bucket=None, domain=None,
                                 ftype=None,
                                 new_region=None):
        """
        获取外网流出流量。可查询当天计量，统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3908/statistic-space
        """
        url = "{0}/v6/blob_io".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, src=src, new_bucket=new_bucket,
                                     new_region=new_region, domain=domain, ftype=ftype)
        ret, info = self.__get(url, options)
        self.blob_put_ret_info(ret, info, select)

    def cdn_traffic_blob_io(self, begin, end, g, select="flow", src="!origin&$src=!atlab&$src=!inner&$src=!ex",
                            new_bucket=None, domain=None,
                            ftype=None,
                            new_region=None):
        """
        获取CDN回源流量统计。可查询当天计量，统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3908/statistic-space
        """
        url = "{0}/v6/blob_io".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, src=src, new_bucket=new_bucket,
                                     new_region=new_region, domain=domain, ftype=ftype)
        ret, info = self.__get(url, options)
        self.blob_put_ret_info(ret, info, select)

    def req_num_blob_io(self, begin, end, g, select="hits", src="origin&$src=inner",
                        new_bucket=None, domain=None,
                        ftype=None,
                        new_region=None):
        """
        获取下载请求次数。可查询当天计量，统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3908/statistic-space
        """
        url = "{0}/v6/blob_io".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, src=src, new_bucket=new_bucket,
                                     new_region=new_region, domain=domain, ftype=ftype)
        ret, info = self.__get(url, options)
        self.blob_put_count_ret_info(ret, info, select)

    def rs_put(self, begin, end, g, select="hits", new_bucket=None, ftype=None, new_region=None):
        """
        获取 PUT 请求次数。可查询当天计量，统计延迟大概 5 分钟。
        https://developer.qiniu.com/kodo/3912/rs-put
        """
        url = "{0}/v6/rs_put".format(config.get_default('default_api_host'))
        options = self.__get_options(begin, end, g, select=select, new_bucket=new_bucket,
                                     new_region=new_region, ftype=ftype)
        ret, info = self.__get(url, options)
        self.blob_put_count_ret_info(ret, info, select)

    def __get(self, url, params=None):
        return http._get_with_qiniu_mac(url, params, self.auth)

    def __get_options(self, begin, end, g, select=None, bucket=None, region=None, no_predel=None, only_predel=None,
                      is_oversea=None,
                      taskid=None, new_bucket=None, new_region=None, ftype=None, domain=None, src=None):
        options = {
            "begin": begin,
            "end": end,
            "g": g,
        }

        if bucket:
            options["bucket"] = bucket
        if region:
            options["region"] = region
        if no_predel:
            options["no_predel"] = 1
        if only_predel:
            options["only_predel"] = 1
        if is_oversea:
            options["$is_oversea"] = is_oversea
        if taskid:
            options["$taskid"] = taskid
        if new_bucket:
            options["$bucket"] = new_bucket
        if new_region:
            options["$region"] = new_region
        if select:
            options["select"] = select
        if ftype:
            options["$ftype"] = ftype
        if domain:
            options["$domain"] = domain
        if src:
            options["$src"] = src

        return options


if __name__ == '__main__':
    access_key = "******"
    secret_key = "******"
    auth = QiniuMacAuth(access_key, secret_key)
    space1 = bucket_Btatistic(auth)
    begin = "20210701"
    end = "20210704"
    g = "day"
    space1.bucket_count_archive(begin=begin, end=end, g=g)
