#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : common.py
# @Date  : 2018/11/2
#@Software : PyCharm
# @Desc  :

import os
import json
import re
import uuid
import codecs
import platform
import subprocess
import webbrowser
import tempfile

from collections import OrderedDict

from config import TMP_DIR
from config import SOAR_ARGS
from config import SOAR_PATH
from config import MUL_SOAR_ARGS
from config import IS_OPEN_BROWESER
from config import DEBUG
from config import SOAR_NOT_USE_ARGS

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def select_soar_for_os_version():
    '''
    获取不同平台 soar 的位置
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
    out_temp = tempfile.SpooledTemporaryFile(max_size=10 * 1000 * 1000)
    sql_tmp_dir = TMP_DIR + os.sep
    try:
        fileno = out_temp.fileno()
        p = subprocess.Popen(cmd, shell=False,cwd=sql_tmp_dir, stdout=fileno,
                             stderr=fileno,universal_newlines=True)
        p.wait() # 如果超时直接干掉
        out_temp.seek(0)
        return out_temp.read().decode('utf8', 'replace')
    except Exception as e:
        # 异常信息会暴露一些系统位置等消息
        raise RuntimeError('run error: %s' % str(e))
    finally:
        if out_temp:
            out_temp.close()


def save_tmp_conf(args,conf_tmp_file):
    '''
    临时配置文件
    :param args:
    :param conf_tmp_file:
    :return:
    '''

    with codecs.open(conf_tmp_file, 'w', encoding='utf8', errors='ignore') as f:
        for arg, value in args.items():
            if isinstance(value,list):
                f.write('%s:\n'%(arg))
                for v in value:
                    f.write('  - %s\n'%(yaml_str(v)))
            elif isinstance(value, dict):
                f.write('%s:\n' % (arg))
                for k,v in value.items():
                    f.write('  %s: %s\n' % (k, yaml_str(v)))
            else:
                f.write('%s: %s\n'%(arg,yaml_str(value)))

# yaml 字符串
def yaml_str(str):
    if str is False or str == 'false':
        return 'false'
    elif str is True or str == 'true':
        return 'true'
    try:
        int(str)
        return str
    except:
        return  "'%s'" % (str.replace("'", "''"))

def save_tmp_blacklist(args,blacklist_tmp_file):
    '''
    临时黑名单文件
    :param args:
    :param blacklist_tmp_file:
    :return:
    '''
    with codecs.open(blacklist_tmp_file, 'w', encoding='utf8', errors='ignore') as f:
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
    conf_tmp_file =soar_run_uuid +'.yaml'
    blacklist_tmp_file= soar_run_uuid +'.blacklist'
    cmd_args=OrderedDict()  # soar 要求 -config 作为第一参数
    log_tmp_file = soar_run_uuid +'.log'

    # sql 美化最大长度为 10k
    args['max-pretty-sql-length'] = 10240;

    # 解析数据库连接
    if 'online-dsn' in args : args['online-dsn'] = dsn2soaryaml(args['online-dsn'])
    if 'test-dsn' in args : args['test-dsn'] = dsn2soaryaml(args['test-dsn'])

    # 黑名单列表
    if 'blacklist' in args:
        save_tmp_blacklist(args, blacklist_tmp_file)
        args['blacklist'] = blacklist_tmp_file
    if 'log-level' in args:
        args['log-output'] = log_tmp_file

    cmd_args['config'] = conf_tmp_file # soar 规定 -config 必须作为第一个参数
    cmd_args['query'] = args['query']
    args.pop('query')

    save_tmp_conf(args, conf_tmp_file)
    cmd_line = req_parse2cmd_parse(cmd_args)

    if DEBUG:
        print(' '.join(cmd_line)) #打印日志信息

    result = runcmd(cmd_line)
    loginfo = ''
    if 'log-level' in args:
        try:
            with codecs.open(log_tmp_file, 'r', encoding='utf8', errors='replace') as f:
                loginfo = f.read()
        except:
            pass

    # 语法检查正确后 soar 无提示,人为提示结果正确
    if 'only-syntax-check' in args and 'true' in args['only-syntax-check'] \
            and result == '':
        return json.dumps({
            "result": '语法正确',
            "status": True,
            "log":loginfo
        })
    if DEBUG is False:
        try:
            # 移除临时配置文件
            os.remove(conf_tmp_file)
            os.remove(blacklist_tmp_file)
            if 'log-level' in args:
                os.remove(log_tmp_file)
        except Exception as e:
                pass
    return json.dumps({
        "result": result,
        "status": True,
        "log": loginfo,
    })

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

# 打开浏览器
def open_brower(url):
    if IS_OPEN_BROWESER:
        try:
            webbrowser.open(url)
        except:
            pass

# 解析dsn
def parse_dsn(dsn):
    try :
        r = r'^(.+)@(.+?)/(.+?)($|\?)(.*)'
        m = re.match(r, dsn)
        if m == None : raise RuntimeError('DSN 解析错误')
        user_info = m.group(1)
        user = user_info.split(':')[0]

        # 为了兼容以前转义的做法, 替换 \
        pwd = re.sub(r'^%s' % user, '', user_info).lstrip(':')\
            .replace('\\\\', '\\').replace('\\@', '@').replace('\\:', ':').replace('\\/', '/')
        host_info = m.group(2)
        host = host_info.split(':')[0]
        port = re.sub(r'^%s' % host, '', host_info).lstrip(':')
        db = m.group(3)
        query = parse_query(m.group(5))
        charset = 'utf8'

        if port == '': port = 3306
        if 'charset' in query : charset = query['charset']
        port = int(port)
    except:
        raise RuntimeError('DSN 解析错误')
    return {
        'host' : host,
        'user' : user,
        'pwd' : pwd,
        'db' : db,
        'port' : port,
        'charset' : charset
    }

# 查询字符串解析
def parse_query(query):
    arr = query.split('&')
    res = {}
    for i in arr :
        paramArr = i.split('=')
        if len(paramArr) == 2 : res[paramArr[0]] = paramArr[1]
    return res

# soar 配置文件
def dsn2soaryaml(dsn):
    dsn = parse_dsn(dsn)
    return {
        'addr' : '%s:%s' % (dsn['host'], dsn['port']),
        'schema' : dsn['db'],
        'user' : dsn['user'],
        'password' : dsn['pwd'],
        'disable' : 'false'
    }
