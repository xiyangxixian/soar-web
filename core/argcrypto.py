#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from config import RSA_PRIVATE_DIR,RSA_PUBLIC_DIR


def en_rsa(message):
    with open(RSA_PUBLIC_DIR,"r") as f:
         key = f.read()
         rsakey = RSA.importKey(key)  # 导入读取到的公钥
         cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象

         # 通过生成的对象加密message明文py3加密的数据是bytes类型的数据，不能是str类型的数据
         return base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))


def de_rsa(cipher_text):
    '''
    RSA 解密
    :param cipher_text:
    :return:
    '''
    with open(RSA_PRIVATE_DIR,'r') as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # 导入读取到的私钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象

        # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        return cipher.decrypt(base64.b64decode(cipher_text), 'ERROR')


def de_aes(key, data):
    '''
    AES 解密
    :param key:
    :param data:
    :return:
    '''
    cryptor = AES.new(key,AES.MODE_CBC,key[:16])
    plain_text = cryptor.decrypt(base64.b64decode(data))
    return plain_text.decode('utf8').replace('\x00','')



def decrypt(data,key):
    '''
    解密
    :param data:
    :param key:
    :return:
    '''
    return de_aes(de_rsa(key),data)
