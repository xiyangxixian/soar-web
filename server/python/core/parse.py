#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : parse.py
# @Author: becivells
#@Contact : becivells@gmail.com
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :
from config import soar_args

def req_parse2cmd_parse(args):
    cmd_args = []
    for arg,v in args.items():
        if v is not None:
            cmd_args.append('-%s %s'%(arg,v))

    return ' '.join(cmd_args)


