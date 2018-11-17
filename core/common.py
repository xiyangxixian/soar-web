#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : common.py
# @Date  : 2018/11/2
#@Software : PyCharm
# @Desc  :

import os
import json
import uuid
import platform
import tempfile
import subprocess
import webbrowser
from collections import OrderedDict

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from config import TMP_DIR
from config import SOAR_ARGS
from config import SOAR_PATH
from config import MUL_SOAR_ARGS
from config import IS_OPEN_BROWESER
from config import DEBUG
from config import SOAR_NOT_USE_ARGS



def select_soar_for_os_version():
    '''
    获取不同平台soar的位置
    :return:
    '''
    os_name = platform.system()
    if(os_name == 'Windows'):
        return 'soar.windows-amd64'
    elif(os_name == 'Linux'):
        return 'soar.linux-amd64'
    elif(os_name == 'Darwin'):
        return 'soar.darwin-amd64'

def req_parse2cmd_parse(args):
    '''
    请求参数转为 soar 命令行
    soar -query xxxx
    :param args:
    :return:
    '''
    soar_path = SOAR_PATH + select_soar_for_os_version()
    cmd_args = [soar_path]
    for arg,value in args.items():
        cmd_args.append('-%s'%(arg))
        cmd_args.append('%s'%(value))

    return cmd_args


def runcmd(cmd):
    '''
    执行外部命令
    :param cmd: 传入列表一个参数为命令，防止命令拼接执行
    :return:
    '''
    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000)
    sql_tmp_dir = TMP_DIR + os.sep
    try:
        fileno = out_temp.fileno()
        p = subprocess.Popen(cmd, shell=False,cwd=sql_tmp_dir, stdout=fileno,
                             stderr=fileno,universal_newlines=True)
        p.wait() # 如果超时直接干掉此函数 py2,py3 不兼容稍后处理
        out_temp.seek(0)
        return out_temp.read()
    except Exception as e:
        # 异常信息会暴露一些系统位置等消息
        return b"run error: %s"%(str(e).encode('utf8'))
    finally:
        if out_temp:
            out_temp.close()

def save_tmp_sql(args,sql_tmp_file):
    '''
    query 转成临时 sql 文件
    :param args:
    :param sql_tmp_file:
    :return:
    '''

    with open(sql_tmp_file,'a') as f:
            f.write(args['query'])

def save_tmp_conf(args,conf_tmp_file):
    '''
    临时配置文件
    :param args:
    :param conf_tmp_file:
    :return:
    '''

    with open(conf_tmp_file,'w') as f:
        for arg, value in args.items():
            if isinstance(value,list):
                f.write('%s:\n'%(arg))
                for v in value:
                    f.write('  - %s\n'%(v))
            else:
                f.write('%s: %s\n'%(arg,value))



def save_tmp_blacklist(args,blacklist_tmp_file):
    '''
    临时黑名单文件
    :param args:
    :param blacklist_tmp_file:
    :return:
    '''
    with open(blacklist_tmp_file,'w') as f:
        for black in args['blacklist'].split('\n'):
            f.write(black)
            f.write('\n')



def soar_result(args):
    '''
    传入请求参数，正确返回执行的结果，错误返回错误信息
    :param args:
    :return:
    '''
    soar_run_uuid = TMP_DIR + str(uuid.uuid1()) # 执行 soar 使用临时缓存路径前缀
    sql_tmp_file =  soar_run_uuid +'.sql'
    conf_tmp_file =soar_run_uuid +'.yaml'
    blacklist_tmp_file= soar_run_uuid +'.blacklist'
    cmd_args=OrderedDict()  # soar 要求 -config 作为第一参数

    if 'blacklist' in args:
        save_tmp_blacklist(args, blacklist_tmp_file)
        args['blacklist'] = blacklist_tmp_file

    save_tmp_sql(args, sql_tmp_file)
    args['query'] = sql_tmp_file

    cmd_args['config'] = conf_tmp_file # soar 规定 -config 必须作为第一个参数

    # 排除 test-dsn online-dsn 继续使用命令行方式字符串代替,主要原因懒的转成序列
    if 'test-dsn' in args:
        cmd_args['test-dsn'] = args['test-dsn']
        args.pop('test-dsn')
    if 'online-dsn' in args:
        cmd_args['online-dsn'] = args['online-dsn']
        args.pop('online-dsn')

    save_tmp_conf(args, conf_tmp_file)
    cmd_line = req_parse2cmd_parse(cmd_args)

    if DEBUG:
        print(' '.join(cmd_line)) #打印日志信息

    result = runcmd(cmd_line).decode('utf8')

    # 语法检查正确后 soar 无提示,人为提示结果正确
    if 'only-syntax-check' in args and 'true' in args['only-syntax-check'] \
            and result == '':
        return json.dumps({
            "result": '语法检查正确', "status": True}
        )
    if DEBUG is False:
        try:
            # 移除临时配置文件
            os.remove(sql_tmp_file)
            os.remove(conf_tmp_file)
            os.remove(blacklist_tmp_file)
        except Exception as e:
                pass
    return json.dumps({
        "result": result, "status": True}
    )

def soar_args_check(args):
    '''
    soar 请求参数检查
    :param args:
    :return:
    '''
    # todo 未做类型检查
    if 'query' not in args and args['query'].strip() == '':
        return json.dumps({'result':'query 参数未指定,或者参数为空','status':False})
    args_error=[]
    for arg,v in args.items():
        if arg not in SOAR_ARGS:
            args_error.append('soar 中没有发现配置: %s,%s '%(arg,args[arg]))
        if arg in MUL_SOAR_ARGS:
            args[arg] = args[arg].split(',') #逗号隔开
        if arg in SOAR_NOT_USE_ARGS:
            args_error.append('soar 此配置禁用: %s,%s ' % (arg, args[arg]))

    if args_error:
       return json.dumps({'result':'\n'.join(args_error),'status':False})

    return None  # 默认不用返回也是 None


def open_brower(url):
    if IS_OPEN_BROWESER:
        webbrowser.open(url)

def parse_dsn(host):
    res = urlparse('http://%s' % host)
    arr = res.netloc.split('@')
    user = 'root'
    pwd = ''
    host = '127.0.0.1'
    port = 3306
    db = res.path.strip('/')
    if len(arr) == 2:
        arr2 = arr[0].split(':')
        host = arr[1]
        if len(arr2) == 2:
            user = arr2[0]
            pwd = arr2[1]
        else:
            user = arr2[0]
    else:
        host = arr[0]
    hostArr = host.split(':')
    host = hostArr[0]
    if (len(hostArr) == 2) : port = hostArr[1]
    return {'host':host, 'user':user, 'pwd':pwd, 'db':db, 'port':int(port), 'charset':''}