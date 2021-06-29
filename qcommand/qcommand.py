# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import fire, logging, os
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

logger = logging.getLogger("qcommand")

_version = Version

pwd_path = os.getcwd()
account_file = "{0}/.qcommand/account.json".format(home_path)


def read_account():
    with open(account_file, "r") as f:
        ret = f.read().split(":")
        accesskey = ret[1]
        secretkey = ret[2]
    return str(accesskey), str(secretkey)


class Qcommand(object):
    """

    """

    @staticmethod
    def account(name="", ak="", sk=""):
        """Get/Set AccessKey and SecretKey"""
        config_path = "{0}/.qcommand".format(home_path)
        if os.path.exists(config_path):
            pass
        else:
            os.mkdir(config_path)
        try:
            account = Account(str(name), str(ak), str(sk))
            account.qcmd_account(config_path)
        except Exception as e:
            logger.warn(e)
            return "qcommand account failed"

    @staticmethod
    def user(args, name=""):
        """Manage users"""
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
        """List all the files in the bucket"""
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                if os.path.exists(outfile):
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
        """"""
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                modtype_success_logpath = os.path.split(successfile)[0]
                modtype_failed_logpath = os.path.split(failurefile)[0]
                if modtype_success_logpath == "{0}/bmodtype".format(
                        pwd_path) and modtype_failed_logpath == "{0}/bmodtype".format(pwd_path):
                    if os.path.exists("{0}/bmodtype".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(modtype_success_logpath)
                if os.path.exists(modtype_success_logpath) and os.path.exists(modtype_failed_logpath):
                    if os.path.exists(inputfile):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                chstatus_success_logpath = os.path.split(successfile)[0]
                chstatus_failed_logpath = os.path.split(failurefile)[0]
                if chstatus_success_logpath == "{0}/bchstatus".format(
                        pwd_path) and chstatus_failed_logpath == "{0}/bchstatus".format(pwd_path):
                    if os.path.exists("{0}/bchstatus".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(chstatus_success_logpath)
                if os.path.exists(chstatus_success_logpath) and os.path.exists(chstatus_failed_logpath):
                    if os.path.exists(inputfile):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                upload_success_logpath = os.path.split(successfile)[0]
                upload_failed_logpath = os.path.split(failurefile)[0]
                if upload_success_logpath == "{0}/bupload".format(
                        pwd_path) and upload_failed_logpath == "{0}/bupload".format(pwd_path):
                    if os.path.exists("{0}/bupload".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(upload_success_logpath)
                if os.path.exists(upload_success_logpath) and os.path.exists(upload_failed_logpath):
                    if os.path.exists(dir):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                upload_success_logpath = os.path.split(successfile)[0]
                upload_failed_logpath = os.path.split(failurefile)[0]
                if upload_success_logpath == "{0}/bdelete".format(
                        pwd_path) and upload_failed_logpath == "{0}/bdelete".format(pwd_path):
                    if os.path.exists("{0}/bdelete".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(upload_success_logpath)
                if os.path.exists(upload_success_logpath) and os.path.exists(upload_failed_logpath):
                    if os.path.exists(inputfile):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                if referer:
                    http_headers = {"Referer": "http://{0}/".format(referer)}
                else:
                    http_headers = {}
                download_success_logpath = os.path.split(successfile)[0]
                download_failed_logpath = os.path.split(failurefile)[0]
                if download_success_logpath == "{0}/bdownload".format(
                        pwd_path) and download_failed_logpath == "{0}/bdownload".format(pwd_path):
                    if os.path.exists("{0}/bdownload".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(download_success_logpath)
                if os.path.exists(download_success_logpath) and os.path.exists(download_failed_logpath):
                    if os.path.exists(inputfile) and os.path.exists(savedir):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                if referer:
                    http_headers = {"Referer": "http://{0}/".format(referer)}
                else:
                    http_headers = {}
                download_success_logpath = os.path.split(successfile)[0]
                download_failed_logpath = os.path.split(failurefile)[0]
                if download_success_logpath == "{0}/bm3u8download".format(
                        pwd_path) and download_failed_logpath == "{0}/bm3u8download".format(pwd_path):
                    if os.path.exists("{0}/bm3u8download".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(download_success_logpath)
                if os.path.exists(download_success_logpath) and os.path.exists(download_failed_logpath):
                    if os.path.exists(inputfile) and os.path.exists(savedir):
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
        try:
            if os.path.exists(account_file):
                accesskey, secretkey = read_account()
                download_success_logpath = os.path.split(successfile)[0]
                download_failed_logpath = os.path.split(failurefile)[0]
                if download_success_logpath == "{0}/bcdnlogdownload".format(
                        pwd_path) and download_failed_logpath == "{0}/bcdnlogdownload".format(pwd_path):
                    if os.path.exists("{0}/bcdnlogdownload".format(pwd_path)):
                        pass
                    else:
                        os.mkdir(download_success_logpath)
                if os.path.exists(download_success_logpath) and os.path.exists(download_failed_logpath):
                    if os.path.exists(savedir):
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
        return ts2d(timestamp)

    @staticmethod
    def uploadtoken(bucket_name, key=None, expires=3600):
        access_key, secret_key = read_account()
        if access_key and secret_key:
            return upload_token(access_key, secret_key, bucket_name, key, expires)
        else:
            return print("Login please enter \"qcommand account --help\" for help")

    @staticmethod
    def version():
        return _version


def main():
    fire.Fire(Qcommand, name="qcommand")


if __name__ == '__main__':
    main()
