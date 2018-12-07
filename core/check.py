#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : soar-api.py.py
# @Author: becivells
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :

import os
import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from config import RSA_PUBLIC_DIR
from config import RSA_PRIVATE_DIR
from config import RSA_PUBLIC_DIR
from config import RSA_PUBLIC_DIR
from config import RSA_PRIVATE_DIR
from config import TMP_DIR
from config import SOAR_PATH



def check_env():
    production_rsa_key()

def production_rsa_key():
    '''
    生成随机秘钥
    :return:
    '''
    random_generator = Random.new().read
    # rsa算法生成实例
    rsa = RSA.generate(1024, random_generator)
    # master的秘钥对的生成
    print('生成秘钥对')
    private_pem = rsa.exportKey()
    with open(RSA_PRIVATE_DIR, 'wb') as f:
        f.write(private_pem)


    public_pem = rsa.publickey().exportKey()
    with open(RSA_PUBLIC_DIR, 'wb') as f:
        f.write(public_pem)

def check_dir():
    pass