# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth
from qiniu import BucketManager
from util import date2timestamp
import logging

logger = logging.getLogger("qcommand")


class Listbucket(object):
    def __init__(self, access_key, secret_key, bucket, file_path, prefix, start, end, fileType,
                 suffix, fsize, stype):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.file_path = file_path
        self.prefix = prefix
        self.start = start
        self.end = end
        self.fileType = fileType
        self.suffix = suffix
        self.fsize = fsize
        self.stype = stype

    def _write_file(self, file_path, i):
        """写入列举信息"""
        for key, value in i.items():
            with open(file_path, "a+") as f:
                if key == "key":
                    f.writelines(str(value) + ",")
                elif key == "fsize":
                    f.writelines(str(value) + ",")
                elif key == "mimeType":
                    f.writelines(str(value) + ",")
                elif key == "putTime":
                    f.writelines(str(value)[:10] + ",")
                elif key == "type":
                    f.writelines(str(value) + ",")
                elif key == "status":
                    f.writelines(str(value) + "\n")

    def _filter_suffix(self, file_path, i, fileType, suffix):
        if ";" in suffix:
            if fileType:
                suffix_tuple = tuple(suffix.split(";"))
                if str(i.get("key")).endswith(suffix_tuple) and str(i.get("mimeType")) in fileType:
                    self._write_file(file_path, i)
            else:
                suffix_tuple = tuple(suffix.split(";"))
                if str(i.get("key")).endswith(suffix_tuple):
                    self._write_file(file_path, i)
        else:
            if fileType:
                if str(i.get("key")).endswith(suffix) and str(i.get("mimeType")) in fileType:
                    self._write_file(file_path, i)
            else:
                if str(i.get("key")).endswith(suffix):
                    self._write_file(file_path, i)

    def _filter_fsize(self, file_path, i, fileType, suffix, fsize):
        """过滤大小为0的文件"""
        if fsize:
            if i.get("fsize") == 0:
                self._write_file(file_path, i)
        else:
            self._filter_filetype_suffix(file_path, i, fileType, suffix)

    def _filter_Storagetype(self, file_path, i, fileType, suffix, fsize, stype):
        if stype == -1:
            self._filter_fsize(file_path, i, fileType, suffix, fsize)
        elif stype == 0:
            if i.get("type") == 0:
                self._filter_fsize(file_path, i, fileType, suffix, fsize)
        elif stype == 1:
            if i.get("type") == 1:
                self._filter_fsize(file_path, i, fileType, suffix, fsize)
        elif stype == 2:
            if i.get("type") == 2:
                self._filter_fsize(file_path, i, fileType, suffix, fsize)

    def _filter_filetype_suffix(self, file_path, i, fileType, suffix):
        """根据文件类型/文件名后缀 过滤文件"""
        if fileType and suffix:
            self._filter_suffix(file_path, i, fileType, suffix)
        elif fileType and suffix is None:
            if str(i.get("mimeType")) in fileType:
                self._write_file(file_path, i)
        elif fileType is None and suffix:
            self._filter_suffix(file_path, i, fileType, suffix)
        else:
            self._write_file(file_path, i)

    def _filter_listinfo(self, ret, file_path, start=None, end=None, fileType=None, suffix=None, fsize=False, stype=-1):
        for i in ret.get("items")[1:]:
            putTime = str(i.get("putTime"))[:10]
            if start and end is None:
                if putTime > start:
                    self._filter_Storagetype(file_path, i, fileType, suffix, fsize, stype)
            elif end and start is None:
                if putTime < end:
                    self._filter_Storagetype(file_path, i, fileType, suffix, fsize, stype)
            elif start and end:
                self._filter_Storagetype(file_path, i, fileType, suffix, fsize, stype)
            else:
                self._filter_Storagetype(file_path, i, fileType, suffix, fsize, stype)

    def _list(self, access_key, secret_key, bucket_name, file_path, prefix, start, end, fileType, suffix, fsize=False,
              stype=-1,
              marker=None, limit=1000,
              delimiter=None):
        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)
        ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
        if eof:
            marker = None
            self._filter_listinfo(ret, file_path, start, end, fileType, suffix, fsize, stype)
        else:
            if info.status_code == 200:
                marker = ret.get("marker")
        return ret, marker, info

    def listBucket(self):
        ret, marker, info = self._list(self.access_key, self.secret_key, self.bucket, self.file_path, self.prefix,
                                       self.start, self.end,
                                       self.fileType, self.suffix, self.fsize, self.stype)
        while True:
            try:
                if info.status_code != 200:
                    return print(
                        "{0},Please check accesskey and secretkey.\nLogin please enter \"qcommand account --help\" for help".format(
                            info.text_body))
                elif marker is None and info.status_code == 200:
                    return print("listbucket success")
                else:
                    ret, marker_new, info = self._list(self.access_key, self.secret_key, self.bucket, self.file_path,
                                                       self.prefix, self.start, self.end,
                                                       self.fileType, self.suffix, self.fsize, self.stype, marker)
                marker = marker_new
            except Exception as e:
                logger.wran(e)
                raise e


if __name__ == '__main__':
    accesskey = "********"
    secretkey = "********"
    bucket = "********"
    outfile = "./123.txt"
    listBucket = Listbucket(accesskey, secretkey, bucket, outfile, prefix=None, start=None, end=None, fileType=None,
                            suffix=None, fsize=False, stype=-1)
    listBucket.listBucket()
