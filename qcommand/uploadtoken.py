# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth


def upload_token(access_key, secret_key, bucket_name, key, expires):
    auth = Auth(access_key, secret_key)
    token = auth.upload_token(bucket_name, key, expires)
    return token
