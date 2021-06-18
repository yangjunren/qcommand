# -*- coding: utf-8 -*-
# flake8: noqa
import lmdb, os, logging
from account import Account
from command_global import home_path

logger = logging.getLogger("qcommand")


class User(object):
    def __init__(self, name):
        self.name = name
        self.account = "{0}/.qcommand/account".format(home_path)

    def qcmd_user_list(self):
        try:
            env = lmdb.open(self.account)
            txn = env.begin()
            ret = ""
            for key, value in txn.cursor():
                value_list = value.decode().split(":")
                ret1 = "\nName:{0}\naccesskey:{1}\nsecretkey:{2}\n".format(key.decode(), value_list[0], value_list[1])
                ret = ret + ret1
            env.close()
            return ret
        except Exception as e:
            logger.warn(e)
            raise e

    def qcmd_user_cu(self):
        if self.name:
            try:
                env = lmdb.open(self.account)
                txn = env.begin()
                val = txn.get(self.name.encode()).decode()
                re = val.split(":")
                os.chdir("{0}/.qcommand".format(home_path))
                Account.account_config(self.name, re[0], re[1])
                ret = "\nName:{0}\naccesskey:{1}\nsecretkey:{2}\n".format(self.name, re[0], re[1])
                env.close()
                return ret
            except Exception as e:
                logger.warn(e)
                raise e
        else:
            return "Name cannot be empty"

    def qcmd_user_remove(self):
        if self.name:
            try:
                env = lmdb.open(self.account)
                txn = env.begin(write=True)
                txn.delete(self.name.encode())
                txn.commit()
                env.close()
            except Exception as e:
                logger.warn(e)
                raise e
        else:
            return "Name cannot be empty"
