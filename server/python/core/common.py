#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : common.py
# @Author: becivells
#@Contact : becivells@gmail.com
# @Date  : 2018/10/31
#@Software : PyCharm
# @Desc  :

import os
import json
import tempfile
import subprocess
from config import BASE_DIR


def runcmd(cmd):
    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
    soar_dir = BASE_DIR + os.sep + 'soar' + os.sep + 'soar.exe '
    sql_tmp_dir = BASE_DIR + os.sep + 'tmp' + os.sep
    try:
        fileno = out_temp.fileno()
        p = subprocess.Popen(soar_dir + cmd, shell=True,cwd=sql_tmp_dir, stdout=fileno, stderr=fileno)
        p.wait()
        out_temp.seek(0)
        return out_temp.read()
    except Exception as e:
        return 'ERROR'
    finally:
        if out_temp:
            out_temp.close()
