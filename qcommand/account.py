# -*- coding: utf-8 -*-
# flake8: noqa
import lmdb, shutil
from logging import getLogger
from os import remove, makedirs, chdir
from os.path import exists, expanduser

logger = getLogger("qcommand")


class Account(object):
    def __init__(self, name, accesskey, secretkey):
        self.name = name
        self.accesskey = accesskey
        self.secretkey = secretkey

    def account_config(self, name, accesskey, secretkey):
        try:
            env = lmdb.open("./account")
            txn = env.begin(write=True)
            txn.put(name.encode(), "{0}:{1}".format(accesskey, secretkey).encode())
            txn.commit()
            env.close()
            if exists("old_account.json"):
                remove("old_account.json")
            elif exists("account.json"):
                shutil.copy("./account.json", "./old_account.json")
            with open("account.json", "w") as f:
                f.write("{0}:{1}:{2}".format(name, accesskey, secretkey))
            logger.debug('qcommand login successfully')
        except Exception as e:
            raise e

    def qcmd_account(self, config_path):
        qcmd_config_path = expanduser(config_path)
        if not exists(qcmd_config_path):
            makedirs(qcmd_config_path)
        try:
            chdir(qcmd_config_path)
            if self.name and self.accesskey and self.secretkey:
                self.account_config(self.name, self.accesskey, self.secretkey)
            elif (self.name and self.accesskey and self.secretkey) is "":
                if exists("account.json"):
                    with open("account.json", "r") as f:
                        l = f.read().split(":")
                        return print("Name:{0}\naccesskey:{1}\nsecretkey:{2}".format(l[0], l[1], l[2]))
                else:
                    logger.warn("Login please enter \"qcommand account --help\" for help")
            else:
                logger.warn("Parameter error, please enter \"qcommand account --help\" for help")
        except Exception as e:
            raise e
