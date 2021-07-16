# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import fire
from logging import getLogger
from os import mkdir, getcwd
from os.path import exists, split
from account import Account
from user import User
from command_global import Version, home_path
from listbucket import Listbucket
from bmodtype import Batch_modtype
from bchstatus import Batch_chstatus
from bupload import Batch_upload
from bdelete import Batch_delete
from bdownload import Batch_download
from b_m3u8_download import B_m3u8_download
from bdownload_cdnlog import Bdownload_cdnlog
from ts2d import ts2d
from uploadtoken import upload_token
from qiniu import QiniuMacAuth, Auth
from bucket_statistic import bucket_Btatistic
from restoreAr import file_restoreAr
from brestoreAr import Batch_restore

logger = getLogger("qcommand")

_version = Version

pwd_path = getcwd()
account_file = "{0}/.qcommand/account.json".format(home_path)


def read_account():
    with open(account_file, "r") as f:
        ret = f.read().split(":")
        accesskey = ret[1]
        secretkey = ret[2]
    return str(accesskey), str(secretkey)


class Qcommand(object):
    @staticmethod
    def account(name="", ak="", sk=""):
        """
        登录七牛账号
        name: 账户的名字, 可以任意取，和在七牛注册的邮箱信息没有关系， 只是qcommand本地用来标示<ak, sk>对
        ak: 七牛账号对应的AccessKey，查看地址：https://portal.qiniu.com/user/key
        sk: 七牛账号对应的SecretKey，查看地址：https://portal.qiniu.com/user/key
        """
        config_path = "{0}/.qcommand".format(home_path)
        if exists(config_path):
            pass
        else:
            mkdir(config_path)
        try:
            account = Account(str(name), str(ak), str(sk))
            account.qcmd_account(config_path)
        except Exception as e:
            logger.warn(e)
            return "qcommand account failed"

    @staticmethod
    def user(args, name=""):
        """
        管理本地用户信息
        args: cu 切换当前的账户，ls 列出所有本地的账户信息，remove 移除特定用户
        name: 账户的名字, qcommand 登录七牛账号时指定的名字。
        """
        try:
            if args == "cu":
                user = User(str(name))
                ret = user.qcmd_user_cu()
                return print(ret)
            if args == "ls":
                user = User(str(name))
                ret = user.qcmd_user_list()
                return ret
            elif args == "remove":
                user = User(str(name))
                user.qcmd_user_remove()
            else:
                return "Parameter error, please enter \"qcommand user --help\" for help"
        except Exception as e:
            raise e

    @staticmethod
    def listbucket(bucket, outfile, prefix=None, start=None, end=None, fileType=None,
                   suffix=None, fsize=False, stype=-1):
        """
        获取七牛空间里面的文件列表，可以指定文件前缀获取指定的文件列表，如果不指定，则获取所有文件的列表。
        bucket: 空间名称，可以为私有空间或者公开空间名称
        outfile: 获取的文件列表保存在本地的文件名
        prefix: 七牛空间中文件名的前缀，该参数为可选参数，如果不指定则获取空间中所有的文件列表
        start: 开始时间，该参数为可选参数，指定后表示列举start时间之后上传的文件，如果不指定则获取空间中所有的文件列表
        end: 结束时间，该参数为可选参数，指定后表示列举end时间之前上传的文件，如果不指定则获取空间中所有的文件列表
        fileType: 七牛空间中文件类型，该参数为可选参数，指定后列举指定类型的文件，如果不指定则获取空间中所有的文件列表
        suffix: 七牛空间中文件名的后缀，该参数为可选参数，指定后列举指定后缀的文件，如果不指定则获取空间中所有的文件列表
        fsize: 七牛空间中文件大小，该参数为可选参数，指定后列举指定大小的文件，如果不指定则获取空间中所有的文件列表
        stype: 七牛空间中文件的存储类型（0 表示标准存储；1 表示低频存储；2 表示归档存储），该参数为可选参数，如果不指定则获取空间中所有的文件列表
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                if exists(outfile):
                    listBucket = Listbucket(accesskey, secretkey, bucket, outfile, prefix, start, end, fileType, suffix,
                                            fsize,
                                            stype)
                    listBucket.listBucket()
                else:
                    return print("outfile:{0}  not exist".format(outfile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bmodtype(bucket, inputfile, sep=",", successfile="{0}/bmodtype/modtype_success.txt".format(pwd_path),
                 failurefile="{0}/bmodtype/modtype_failed.txt".format(pwd_path), threadcount=3):
        """
        批量修改空间中的文件 存储类型。
        bucket: 空间名称，可以为公开空间或者私有空间
        inputfile: 包含文件名和存储类型的txt文件
        sep: inputfile 文件中 需要修改存储类型的文件名与存储类型（0 表示标准存储；1 表示低频存储；2 表示归档存储）之间的分割符（默认是,分割）
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bmodtype 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bmodtype 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                modtype_success_logpath = split(successfile)[0]
                modtype_failed_logpath = split(failurefile)[0]
                if modtype_success_logpath == "{0}/bmodtype".format(
                        pwd_path) and modtype_failed_logpath == "{0}/bmodtype".format(pwd_path):
                    if exists("{0}/bmodtype".format(pwd_path)):
                        pass
                    else:
                        mkdir(modtype_success_logpath)
                if exists(modtype_success_logpath) and exists(modtype_failed_logpath):
                    if exists(inputfile):
                        Batch = Batch_modtype(accesskey, secretkey, bucket, inputfile, sep, successfile,
                                              failurefile,
                                              threadcount)
                        Batch.b_modtype()
                    else:
                        return print("inputfile:{0} not exist".format(inputfile))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bchstatus(bucket, inputfile, sep=",", successfile="{0}/bchstatus/chstatus_success.txt".format(pwd_path),
                  failurefile="{0}/bchstatus/chstatus_failed.txt".format(pwd_path), threadcount=3):
        """
        批量修改文件状态（0表示启用，1表示禁用）
        bucket: 空间名称，可以为公开空间或者私有空间
        inputfile: 包含文件名和文件状态的txt文件
        sep: inputfile 文件中 需要修改存储类型的文件名与存储类型（0 表示标准存储；1 表示低频存储；2 表示归档存储）之间的分割符（默认是,分割）。
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bchstatus 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bchstatus 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                chstatus_success_logpath = split(successfile)[0]
                chstatus_failed_logpath = split(failurefile)[0]
                if chstatus_success_logpath == "{0}/bchstatus".format(
                        pwd_path) and chstatus_failed_logpath == "{0}/bchstatus".format(pwd_path):
                    if exists("{0}/bchstatus".format(pwd_path)):
                        pass
                    else:
                        mkdir(chstatus_success_logpath)
                if exists(chstatus_success_logpath) and exists(chstatus_failed_logpath):
                    if exists(inputfile):
                        Batch = Batch_chstatus(accesskey, secretkey, bucket, inputfile, sep, successfile,
                                               failurefile,
                                               threadcount)
                        Batch.batch_chstatus()
                    else:
                        return print("inputfile:{0} not exist".format(inputfile))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bupload(bucket, dir, successfile="{0}/bupload/upload_success.txt".format(pwd_path),
                failurefile="{0}/bupload/upload_failed.txt".format(pwd_path), threadcount=3):
        """
        批量上传文件
        bucket: 空间名称，可以为公开空间或者私有空间
        dir: 需要上传的文件目录
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的bupload目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的bupload目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                upload_success_logpath = split(successfile)[0]
                upload_failed_logpath = split(failurefile)[0]
                if upload_success_logpath == "{0}/bupload".format(
                        pwd_path) and upload_failed_logpath == "{0}/bupload".format(pwd_path):
                    if exists("{0}/bupload".format(pwd_path)):
                        pass
                    else:
                        mkdir(upload_success_logpath)
                if exists(upload_success_logpath) and exists(upload_failed_logpath):
                    if exists(dir):
                        Batch = Batch_upload(accesskey, secretkey, dir, bucket, successfile, failurefile,
                                             threadcount)
                        Batch.batch_upload()
                    else:
                        return print("dir:{0}  not exist".format(dir))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bdelete(bucket, inputfile, successfile="{0}/bdelete/delete_success.txt".format(pwd_path),
                failurefile="{0}/bdelete/delete_failed.txt".format(pwd_path), threadcount=3):
        """
        批量删除文件
        bucket: 空间名称，可以为公开空间或者私有空间
        inputfile: 包含文件名的txt文件
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdelete 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdelete 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                upload_success_logpath = split(successfile)[0]
                upload_failed_logpath = split(failurefile)[0]
                if upload_success_logpath == "{0}/bdelete".format(
                        pwd_path) and upload_failed_logpath == "{0}/bdelete".format(pwd_path):
                    if exists("{0}/bdelete".format(pwd_path)):
                        pass
                    else:
                        mkdir(upload_success_logpath)
                if exists(upload_success_logpath) and exists(upload_failed_logpath):
                    if exists(inputfile):
                        Batch = Batch_delete(accesskey, secretkey, bucket, inputfile, successfile, failurefile,
                                             threadcount)
                        Batch.batch_delete()
                    else:
                        return print("inputfile:{0} not exist".format(inputfile))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bdownload(domain, inputfile, savedir, referer=None, private=False,
                  successfile="{0}/bdownload/download_success.txt".format(pwd_path),
                  failurefile="{0}/bdownload/download_failed.txt".format(pwd_path), threadcount=3):
        """
        批量下载空间文件
        domain: 空间绑定的域名，可以为公开空间或者私有空间
        inputfile: 包含文件名的txt文件
        savedir: 文件保存路径
        referer: referer参数，domain域名开启referer白名单的情况下设置，设置一个白名单中的域名即可
        private: 空间属性，bool类型，默认为False（公开空间），私有空间的话置为True
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdownload 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bdownload 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                if referer:
                    http_headers = {"Referer": "http://{0}/".format(referer)}
                else:
                    http_headers = {}
                download_success_logpath = split(successfile)[0]
                download_failed_logpath = split(failurefile)[0]
                if download_success_logpath == "{0}/bdownload".format(
                        pwd_path) and download_failed_logpath == "{0}/bdownload".format(pwd_path):
                    if exists("{0}/bdownload".format(pwd_path)):
                        pass
                    else:
                        mkdir(download_success_logpath)
                if exists(download_success_logpath) and exists(download_failed_logpath):
                    if exists(inputfile) and exists(savedir):
                        Batch = Batch_download()
                        Batch.batch_download(accesskey, secretkey, domain, inputfile, savedir, http_headers, private,
                                             successfile, failurefile,
                                             threadcount)
                    else:
                        return print("inputfile:{0} or savedir:{1} not exist".format(inputfile, savedir))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bm3u8(domain, inputfile, savedir, referer=None, private=False,
              successfile="{0}/bm3u8download/download_success.txt".format(pwd_path),
              failurefile="{0}/bm3u8download/download_failed.txt".format(pwd_path), threadcount=3):
        """
        下载m3u8文件
        domain: 空间绑定的域名，可以为公开空间或者私有空间
        inputfile: 包含m3u8文件名的txt文件
        savedir: 文件保存路径
        referer: referer参数，domain域名开启referer白名单的情况下设置，设置一个白名单中的域名即可
        private: 空间属性，bool类型，默认为False（公开空间），私有空间的话置为True
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bm3u8download 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bm3u8download 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                if referer:
                    http_headers = {"Referer": "http://{0}/".format(referer)}
                else:
                    http_headers = {}
                download_success_logpath = split(successfile)[0]
                download_failed_logpath = split(failurefile)[0]
                if download_success_logpath == "{0}/bm3u8download".format(
                        pwd_path) and download_failed_logpath == "{0}/bm3u8download".format(pwd_path):
                    if exists("{0}/bm3u8download".format(pwd_path)):
                        pass
                    else:
                        mkdir(download_success_logpath)
                if exists(download_success_logpath) and exists(download_failed_logpath):
                    if exists(inputfile) and exists(savedir):
                        Batch = B_m3u8_download(accesskey, secretkey, domain, inputfile, savedir, http_headers, private,
                                                successfile, failurefile,
                                                threadcount)
                        Batch.batch_m3u8_download()
                    else:
                        return print("inputfile:{0} or savedir:{1} not exist".format(inputfile, savedir))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def bcdnlog(date, domains, savedir,
                successfile="{0}/bcdnlogdownload/download_success.txt".format(pwd_path),
                failurefile="{0}/bcdnlogdownload/download_failed.txt".format(pwd_path), threadcount=3):
        """
        下载CDN日志
        date: 日期，例如 2016-07-01
        domains: 域名，多个域名用;分割，示例 123.qiniu.com;345.test.com
        savedir: 文件保存路径
        successfile: 处理成功的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bcdnlogdownload 目录下
        failurefile: 处理失败的文件记录，可选参数，不指定，默认保存在 qcommand 运行目录的 bcdnlogdownload 目录下
        threadcount: 并发数，可选参数，默认值为3
        """
        try:
            if exists(account_file):
                accesskey, secretkey = read_account()
                download_success_logpath = split(successfile)[0]
                download_failed_logpath = split(failurefile)[0]
                if download_success_logpath == "{0}/bcdnlogdownload".format(
                        pwd_path) and download_failed_logpath == "{0}/bcdnlogdownload".format(pwd_path):
                    if exists("{0}/bcdnlogdownload".format(pwd_path)):
                        pass
                    else:
                        mkdir(download_success_logpath)
                if exists(download_success_logpath) and exists(download_failed_logpath):
                    if exists(savedir):
                        Batch = Bdownload_cdnlog(accesskey, secretkey, domains, date, savedir,
                                                 successfile, failurefile,
                                                 threadcount)
                        Batch.batch_download_cdnlog()
                    else:
                        return print("savedir:{0} not exist".format(savedir))
                else:
                    return print("successfile:{0} or failurefile:{1} not exist".format(successfile, failurefile))
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def ts2d(timestamp):
        """
        时间戳转日期
        timestamp: 时间戳，单位：秒。
        """
        return ts2d(timestamp)

    @staticmethod
    def uploadtoken(bucket_name, key=None, expires=3600):
        """
        获取上传token
        bucket_name: 空间名
        key: 文件名，可选参数。
        expires: token有效期，默认有效期 3600秒
        """
        access_key, secret_key = read_account()
        if access_key and secret_key:
            return upload_token(access_key, secret_key, bucket_name, key, expires)
        else:
            return print("Login please enter \"qcommand account --help\" for help")

    @staticmethod
    def space(begin, end, g, bucket=None, region=None, outfile=None):
        """
        获取标准存储的存储量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_space(begin=begin, end=end, g=g, bucket=bucket, region=region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def count(begin, end, g, bucket=None, region=None, outfile=None):
        """
        获取标准存储的文件数量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_count(begin=begin, end=end, g=g, bucket=bucket, region=region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def spaceline(begin, end, g, bucket=None, region=None, no_predel=False, only_predel=False, outfile=None):
        """
        获取低频存储的当前存储量。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        no_predel: 除去低频存储提前删除，剩余的存储量。可选参数，默认为 False，包含提前删除存储量。置为True时，不包含提前删除存储量。
        only_predel: 只显示低频存储提前删除的存储量。可选参数，默认为 False，显示所有存储量。置为True时，只显示提前删除存储量。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_space_line(begin=begin, end=end, g=g, bucket=bucket, region=region, no_predel=no_predel,
                                        only_predel=only_predel, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def countline(begin, end, g, bucket=None, region=None, outfile=None):
        """
        获取低频存储的文件数量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_count_line(begin=begin, end=end, g=g, bucket=bucket, region=region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def spacearchive(begin, end, g, bucket=None, region=None, no_predel=False, only_predel=False, outfile=None):
        """
        获取低频存储的文件数量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        no_predel: 除去归档存储提前删除，剩余的存储量。可选参数，默认为 False，包含提前删除存储量。置为True时，不包含提前删除存储量。
        only_predel: 只显示归档存储提前删除的存储量。可选参数，默认为 False，显示所有存储量。置为True时，只显示提前删除存储量。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_space_archive(begin=begin, end=end, g=g, bucket=bucket, region=region, no_predel=no_predel,
                                           only_predel=only_predel, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def countarchive(begin, end, g, bucket=None, region=None, outfile=None):
        """
        获取归档存储的文件数量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        bucket: 存储空间名称，是一个条件请求参数。可选参数，不指定默认获取所有。
        region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.bucket_count_archive(begin=begin, end=end, g=g, bucket=bucket, region=region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def blobtransfer(begin, end, g, is_oversea=None, taskid=None, outfile=None):
        """
        获取跨区域同步流量统计数据。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        is_oversea: 是否为海外同步,0 国内,1 海外。可选参数，不填表示查询总跨区域同步流量
        taskid: 任务 id。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.blob_transfer(begin=begin, end=end, g=g, is_oversea=is_oversea, taskid=taskid, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def rschtype(begin, end, g, new_bucket=None, new_region=None, outfile=None):
        """
        获取存储类型转换请求次数。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        new_bucket: 空间名称是一个条件请求参数。可选参数，不指定默认获取所有。
        new_region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.rs_chtype(begin=begin, end=end, g=g, new_bucket=new_bucket, new_region=new_region,
                                outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def rsput(begin, end, g, new_bucket=None, ftype=None, new_region=None, outfile=None):
        """
        获取 PUT 请求次数。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        new_bucket: 空间名称是一个条件请求参数。可选参数，不指定默认获取所有。
        ftype: 存储类型，0 标准存储，1 低频存储，2 归档存储。可选参数，不指定默认获取所有
        new_region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.rs_put(begin=begin, end=end, g=g, new_bucket=new_bucket, new_region=new_region, ftype=ftype,
                             outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def internet_traffic(begin, end, g, new_bucket=None, domain=None, ftype=None, new_region=None, outfile=None):
        """
        获取外网流出流量。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        new_bucket: 空间名称是一个条件请求参数。可选参数，不指定默认获取所有。
        domain: 空间访问域名。可选参数
        ftype: 存储类型，0 标准存储，1 低频存储，2 归档存储。可选参数，不指定默认获取所有
        new_region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.internet_traffic_blob_io(begin=begin, end=end, g=g, new_bucket=new_bucket, domain=domain,
                                               ftype=ftype,
                                               new_region=new_region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def cdn_traffic(begin, end, g, new_bucket=None, domain=None, ftype=None, new_region=None, outfile=None):
        """
        获取CDN回源流量统计。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        new_bucket: 空间名称是一个条件请求参数。可选参数，不指定默认获取所有。
        domain: 空间访问域名。可选参数
        ftype: 存储类型，0 标准存储，1 低频存储，2 归档存储。可选参数，不指定默认获取所有
        new_region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.cdn_traffic_blob_io(begin=begin, end=end, g=g, new_bucket=new_bucket, domain=domain,
                                          ftype=ftype,
                                          new_region=new_region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def req_num(begin, end, g, new_bucket=None, domain=None, ftype=None, new_region=None, outfile=None):
        """
        获取下载请求次数。可查询当天计量，统计延迟大概 5 分钟。
        begin: 起始日期字符串，闭区间，例如： 20060102150405
        end: 结束日期字符串，开区间，例如： 20060102150405
        g: 时间粒度，支持 day；当天支持5min、hour、day
        new_bucket: 空间名称是一个条件请求参数。可选参数，不指定默认获取所有。
        domain: 空间访问域名。可选参数
        ftype: 存储类型，0 标准存储，1 低频存储，2 归档存储。可选参数，不指定默认获取所有
        new_region: 存储区域，z0 华东，z1 华北，z2 华南，na0 北美，as0 东南亚，cn-east-2 华东-浙江2。可选参数，不指定默认获取所有。
        outfile: 查询结果保存位置，可选参数。默认直接打印显示。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = QiniuMacAuth(access_key, secret_key)
                space = bucket_Btatistic(auth)
                space.req_num_blob_io(begin=begin, end=end, g=g, new_bucket=new_bucket, domain=domain,
                                      ftype=ftype,
                                      new_region=new_region, outfile=outfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def restore(bucket, key, days):
        """
        解冻单个归档文件
        bucket: 归档文件所在空间
        key: 需要解冻的文件名
        days: 解冻时长，单位天，范围 1-7
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                file_restoreAr(access_key, secret_key, bucket, key, days)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def brestore(bucket, inputfile, days=7, resfile=None):
        """
        批量解冻 归档文件
        bucket: 归档文件所在空间
        inputfile: 包含归档文件名的 txt文件
        days: 解冻时长，单位天，范围 1-7，可选参数，默认解冻时长为7天。
        resfile: 处理结果保存文件路径，可选参数。默认保存在qcommand运行目录，文件名为 resfile_{bucket}.txt。
        """
        try:
            if exists(account_file):
                access_key, secret_key = read_account()
                auth = Auth(access_key, secret_key)
                batch_restore = Batch_restore(auth)
                if resfile is None:
                    resfile = "./resfile_{0}.txt".format(bucket)
                batch_restore.batch_restore(bucket, inputfile, days, resfile)
            else:
                return print("Login please enter \"qcommand account --help\" for help")
        except Exception as e:
            logger.warn(e)
            raise e

    @staticmethod
    def version():
        return _version


def main():
    fire.Fire(Qcommand, name="qcommand")


if __name__ == '__main__':
    main()
